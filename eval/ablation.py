import json
import os
from core.pipeline import TranslationPipeline

def run_ablation():
    """
    Runs pipeline with and without normalization to compare outputs.
    Note: Since our pipeline integrates normalization deeply, 
    we will simulate 'OFF' by bypassing the normalizer manually or modifying config.
    """
    pipeline = TranslationPipeline()
    
    test_cases = [
        "Main aaj bahut happy hoon", # Hinglish
        "bindass perform karo",       # Slang
        "kya haal hai"               # Transliteration
    ]
    
    results = []
    
    print("Running Ablation Study...")
    
    for text in test_cases:
        # Full Pipeline
        full_out = pipeline.translate(text, target_lang="Hindi")
        
        # Ablated (No Norm)
        # We manually just call the model without norm
        # This is a bit hacky but valid for ablation demo
        no_norm_out = "N/A"
        try:
            tokenizer, model = pipeline.load_model(pipeline.config["DEFAULT_MODEL_EN_HI"])
            if tokenizer and model:
                inputs = tokenizer(text, return_tensors="pt", padding=True)
                translated = model.generate(**inputs)
                no_norm_out = tokenizer.decode(translated[0], skip_special_tokens=True)
        except:
            pass
            
        results.append({
            "input": text,
            "with_normalization": full_out["translation"],
            "without_normalization": no_norm_out
        })
        
    # Save
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
        
    with open("outputs/ablation_results.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print("Ablation complete. Results saved to outputs/ablation_results.json")

if __name__ == "__main__":
    run_ablation()
