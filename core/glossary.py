import csv
import re
import pandas as pd
from typing import Dict, List, Tuple

class GlossaryManager:
    def __init__(self, glossary_path: str = None):
        self.glossary: Dict[str, str] = {}
        if glossary_path:
            self.load_glossary(glossary_path)

    def load_glossary(self, path: str):
        """Loads glossary from a CSV file (Source, Target)."""
        try:
            df = pd.read_csv(path)
            # Expecting columns 'Source' and 'Target'
            if 'Source' in df.columns and 'Target' in df.columns:
                self.glossary = pd.Series(df.Target.values, index=df.Source.values).to_dict()
            else:
                print(f"Warning: CSV must have 'Source' and 'Target' columns. Found: {df.columns}")
        except Exception as e:
            print(f"Error loading glossary: {e}")

    def apply_glossary_pre_translation(self, text: str) -> Tuple[str, List[str]]:
        """
        Marks glossary terms to prevent translation (placeholder strategy) 
        OR prepares them for post-editing.
        For simple replacement, we might not do much here unless we use specific tokens.
        """
        # A simple strategy: We will just track them for now or use a placeholder if need be.
        # For this demo, we will rely on post-translation enforcement or simple substitution if languages match.
        return text, []

    def apply_glossary_post_translation(self, translated_text: str, source_text: str) -> str:
        """
        Enforce glossary terms in the output.
        This is tricky for morphology (e.g. 'Bank' -> 'Bankon').
        For this MVP, we do a direct replacement if the target term is strict.
        """
        # Simple string replacement for demo purposes.
        # Ideally, we should check if the source term existed in source_text before forcing it in target,
        # but here we assume the glossary maps Source Language Term -> Target Language Term.
        
        # We iterate through the glossary and check if the 'Source' term was likely the topic.
        # A better approach for the demo: Just ensure the 'Target' word exists if 'Source' word was in input.
        
        final_text = translated_text
        for source_term, target_term in self.glossary.items():
            # If source term is present in the original text (case-insensitive)
            if re.search(r'\b' + re.escape(str(source_term)) + r'\b', source_text, re.IGNORECASE):
                # We want to ensure target_term is in final_text.
                # But we don't know WHERE to put it without alignment.
                # So we will use a naive Replace All from the default translation of that term if possible.
                # LIMITATION: This is hard without word alignment. 
                # Fallback: We can just use this for "Do Not Translate" (Keep English in Hindi output).
                
                # Case 1: Keep original term (Source == Target)
                if source_term.lower() == target_term.lower():
                     # If the model translated it, we might try to revert it.
                     # This is hard to guess what it translated to.
                     pass 
                
        return final_text

    def simple_replace(self, text: str) -> str:
        """
        Directly replaces occurrences of Source with Target.
        Useful if we want to force specific vocabulary before processing or in the output.
        """
        for source, target in self.glossary.items():
            pattern = re.compile(r'\b' + re.escape(str(source)) + r'\b', re.IGNORECASE)
            text = pattern.sub(str(target), text)
        return text
