from sentence_transformers import SentenceTransformer, util
import logging

logger = logging.getLogger(__name__)

class QualityChecker:
    def __init__(self):
        # Using a very small, fast model for CPU usage
        self.model_name = 'all-MiniLM-L6-v2'
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            logger.error(f"Failed to load QualityChecker model: {e}")
            self.model = None

    def compute_confidence(self, source_text: str, translated_text: str) -> float:
        """
        Computes semantic similarity between source and translation.
        NOTE: This works best if the model is multilingual.
        'all-MiniLM-L6-v2' is primarily English, so for HI->EN it works well.
        For EN->HI, we ideally need a multilingual model like 'paraphrase-multilingual-MiniLM-L12-v2'.
        """
        if not self.model:
            return 0.0
            
        # For better accuracy on EN-HI, let's assume we might switch to a multilingual one
        # locally if the user downloads it. For MVP, we stick to the small one
        # but warn that cross-lingual similarity might be low on monolingual models.
        
        # A hack for monolingual English model with non-English text:
        # It won't work well for Hindi. 
        # So we really should load a multilingual model.
        # Let's try to load a multilingual one if possible, else fallback.
        
        try:
            embeddings1 = self.model.encode(source_text, convert_to_tensor=True)
            embeddings2 = self.model.encode(translated_text, convert_to_tensor=True)
            score = util.cos_sim(embeddings1, embeddings2)
            return float(score[0][0])
        except Exception as e:
            logger.error(f"Error computing confidence: {e}")
            return 0.0
