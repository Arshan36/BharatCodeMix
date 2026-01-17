import re
from typing import Dict, Tuple

class LanguageDetector:
    def __init__(self):
        # A small set of common English words to help distinguish Hinglish from English
        self.common_english_words = {
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with",
            "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
            "is", "are", "was", "were"
        }

    def detect_script(self, text: str) -> str:
        """Detects if the text is predominantly Devanagari or Latin."""
        devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
        latin_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if devanagari_chars > latin_chars:
            return "Devanagari"
        return "Latin"

    def detect_language(self, text: str) -> str:
        """
        Heuristic detection for English vs Hinglish (Romanized Hindi).
        Strategy: Check ratio of common English stop words.
        """
        script = self.detect_script(text)
        if script == "Devanagari":
            return "Hindi"
        
        # If Latin, check if it looks like English or Hinglish
        words = re.sub(r'[^\w\s]', '', text.lower()).split()
        if not words:
            return "English"
            
        english_word_count = sum(1 for w in words if w in self.common_english_words)
        ratio = english_word_count / len(words)
        
        # If less than 20% of words are common English stop words, assume Hinglish
        # This is a rough heuristic but works for many short sentences.
        if ratio < 0.2:
            return "Hinglish"
        return "English"
