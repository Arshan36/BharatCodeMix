import json
import re
import os
from indic_transliteration import sanscript
from indic_transliteration import sanscript

class Normalizer:
    def __init__(self, slang_map_path: str = None):
        self.slang_map = {}
        if slang_map_path and os.path.exists(slang_map_path):
            with open(slang_map_path, 'r', encoding='utf-8') as f:
                self.slang_map = json.load(f)
        else:
            # Fallback inline default
            self.slang_map = {
                "bindass": "carefree",
                "jugaad": "hack",
                "sem": "semester",
                "prof": "professor"
            }

    def normalize_slang(self, text: str) -> str:
        """Replaces known slang words with formal alternatives."""
        words = text.split()
        normalized_words = []
        for word in words:
            lower_word = word.lower().strip(".,!?")
            if lower_word in self.slang_map:
                # Replace but try to keep casing if original was Capitalized
                replacement = self.slang_map[lower_word]
                if word[0].isupper():
                    replacement = replacement.capitalize()
                normalized_words.append(replacement)
            else:
                normalized_words.append(word)
        return " ".join(normalized_words)

    def transliterate_to_devanagari(self, text: str) -> str:
        """
        Converts Romanized Hindi (ITRANS/Velthuis-like) to Devanagari.
        Using a standard scheme (ITRANS) as a best-effort approximation for "chat style" Hindi.
        Note: True "Hinglish to Hindi" requires a seq2seq model, but we use rule-based for this constraint.
        """
        # We'll use HK (Harvard-Kyoto) or ITRANS. HK is often simpler for general chat typing.
        # Let's try to trust the library's best effort for Roman -> Devanagari.
        try:
            return sanscript.transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
        except Exception:
            return text
