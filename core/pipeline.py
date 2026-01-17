import os
import logging
from .utils import load_config
from .lang_detect import LanguageDetector
from .normalize import Normalizer
from .glossary import GlossaryManager
from .quality_check import QualityChecker
from transformers import MarianMTModel, MarianTokenizer

logger = logging.getLogger(__name__)

class TranslationPipeline:
    def __init__(self):
        self.config = load_config()
        self.lang_detector = LanguageDetector()
        self.normalizer = Normalizer("data/slang_map.json")
        self.glossary_manager = GlossaryManager("data/glossary_example.csv")
        self.quality_checker = QualityChecker()
        
        # Cache for models
        self.models = {}
        self.tokenizers = {}

    def load_model(self, model_name):
        if model_name not in self.models:
            logger.info(f"Loading model: {model_name}")
            try:
                self.tokenizers[model_name] = MarianTokenizer.from_pretrained(model_name)
                self.models[model_name] = MarianMTModel.from_pretrained(model_name)
            except Exception as e:
                logger.error(f"Failed to load model {model_name}: {e}")
        return self.tokenizers.get(model_name), self.models.get(model_name)

    def translate(self, text, source_lang_hint=None, target_lang="Hindi"):
        """
        Main pipeline execution.
        """
        steps_log = {}

        # 1. Detection
        detected_script = self.lang_detector.detect_script(text)
        detected_lang = self.lang_detector.detect_language(text)
        steps_log["detected_script"] = detected_script
        steps_log["detected_lang"] = detected_lang

        # 2. Normalization
        normalized_text = text
        if detected_lang == "Hinglish" or detected_script == "Latin":
            # Apply slang normalization first
            normalized_text = self.normalizer.normalize_slang(normalized_text)
            steps_log["slang_normalized"] = normalized_text
            
            # Then transliterate if going to Hindi and script is Latin
            # For MarianMT EN->HI, it expects English script.
            # But if it's "Hinglish" (Hindi content in English script), we might want to:
            # A) Translate EN words -> Hindi
            # B) Transliterate HI words -> Hindi script
            
            # The prompt asks for: "Code-mix input... Normalization (Latin->Devanagari where needed)"
            # A naive approach for Hinglish -> Hindi is typically:
            # Transliterate everything to Devanagari -> Then allow model to handle it?
            # actually MarianMT EN-HI expects English input.
            # If input is "kya haal hai" (Hinglish), and we send it to EN-HI model, it might fail.
            # If we transliterate to "क्या हाल है", we verify it IS Hindi.
            
            if target_lang == "Hindi":
               # If it was classified as Hinglish, we might assume it is mostly Hindi in Latin script.
               # In that case, the 'translation' is effectively Transliteration + Grammar fix.
               # BUT, if we have a model EN->HI, and we give it "Happy Birthday", it gives "janmdin mubarak".
               # If we give "Tum kahan ho", it might translate "Tum" as "You" ?? No, standard models fail on Hinglish.
               
               # Demo Strategy:
               # If Hinglish is detected, we prioritize Transliteration to Devanagari
               # and treat THAT as the output if the goal is Hindi.
               # IF the goal is English, we transliterate to Devanagari -> Translate HI to EN.
               
               pass

        # Apply Glossary (Pre) - keeping specific terms
        normalized_text, _ = self.glossary_manager.apply_glossary_pre_translation(normalized_text)
        
        # 3. Translation
        final_translation = ""
        model_name = ""
        
        # Logic for Model Selection
        # Case 1: English -> Hindi
        if (detected_lang == "English") and target_lang == "Hindi":
            model_name = self.config["DEFAULT_MODEL_EN_HI"]
            
        # Case 2: Hindi (Devanagari) -> English
        elif (detected_lang == "Hindi" or detected_script == "Devanagari") and target_lang == "English":
            model_name = self.config["DEFAULT_MODEL_HI_EN"]
            
        # Case 3: Hinglish (Latin) -> Hindi
        elif (detected_lang == "Hinglish") and target_lang == "Hindi":
            # Just transliterate
            transliterated = self.normalizer.transliterate_to_devanagari(normalized_text)
            steps_log["transliteration"] = transliterated
            final_translation = transliterated
            # We skip neural translation here as it's already "translated" script-wise.
            
        # Case 4: Hinglish (Latin) -> English
        elif (detected_lang == "Hinglish") and target_lang == "English":
            # Transliterate to Devanagari -> Then Translate HI to EN
            transliterated = self.normalizer.transliterate_to_devanagari(normalized_text)
            steps_log["transliteration"] = transliterated
            normalized_text = transliterated # New input for translation
            model_name = self.config["DEFAULT_MODEL_HI_EN"]
            
        else:
            # Fallback or identity
            final_translation = normalized_text

        # Run Neural Model if needed
        if model_name:
            tokenizer, model = self.load_model(model_name)
            if tokenizer and model:
                try:
                    inputs = tokenizer(normalized_text, return_tensors="pt", padding=True)
                    translated = model.generate(**inputs)
                    final_translation = tokenizer.decode(translated[0], skip_special_tokens=True)
                except Exception as e:
                    logger.error(f"Translation failed: {e}")
                    final_translation = "Error in translation"

        steps_log["raw_translation"] = final_translation

        # 4. Glossary (Post)
        final_translation = self.glossary_manager.apply_glossary_post_translation(final_translation, text)
        steps_log["glossary_applied"] = final_translation

        # 5. Quality Check
        confidence = self.quality_checker.compute_confidence(text, final_translation)
        
        return {
            "original": text,
            "normalized": normalized_text,
            "translation": final_translation,
            "confidence": confidence,
            "logs": steps_log
        }
