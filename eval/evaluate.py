import argparse
import json
import logging
import os
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
# For chrF, we usually use sacrebleu or manual calculation. NLTK CHRF is also an option.
from nltk.translate.chrf_score import sentence_chrf
from core.pipeline import TranslationPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_evaluation(smoke=False):
    pipeline = TranslationPipeline()
    
    # Load dataset
    data_path = "data/sample_inputs.json"
    with open(data_path, 'r') as f:
        data = json.load(f)
        
    if smoke:
        data = data[:3]
        
    results = []
    total_bleu = 0
    total_chrf = 0
    count = 0
    
    print(f"Running evaluation on {len(data)} examples...")
    
    for item in data:
        src = item["text"]
        src_lang = item.get("source_lang", "English")
        tgt_lang = item.get("target_lang", "Hindi")
        
        # Note: In a real eval, we need reference translations.
        # Since we don't have them in 'sample_inputs.json', we will skip metrics or mock them 
        # unless 'reference' key exists.
        reference = item.get("reference", "")
        
        output = pipeline.translate(src, source_lang_hint=src_lang, target_lang=tgt_lang)
        translation = output["translation"]
        
        bleu = 0
        chrf = 0
        
        if reference:
            # BLEU
            ref_tokens = reference.split()
            hyp_tokens = translation.split()
            smooth = SmoothingFunction().method1
            bleu = sentence_bleu([ref_tokens], hyp_tokens, smoothing_function=smooth)
            
            # CHRF
            chrf = sentence_chrf(reference, translation)
            
            total_bleu += bleu
            total_chrf += chrf
            count += 1
            
        results.append({
            "source": src,
            "prediction": translation,
            "reference": reference,
            "bleu": bleu,
            "chrf": chrf,
            "confidence": output["confidence"]
        })
        
        print(f"SRC: {src} -> TGT: {translation} (Conf: {output['confidence']:.2f})")

    if count > 0:
        avg_bleu = total_bleu / count
        avg_chrf = total_chrf / count
        print(f"\nAverage BLEU: {avg_bleu:.4f}")
        print(f"Average chrF: {avg_chrf:.4f}")
    else:
        print("\nNo references found for metrics calculation. Just ran inference.")

    # Save results
    with open("outputs/eval_results.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true", help="Run quick smoke test")
    args = parser.parse_args()
    
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
        
    run_evaluation(smoke=args.smoke)
