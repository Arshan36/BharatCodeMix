import gradio as gr
import os
from core.pipeline import TranslationPipeline
from core.stt import STT
from core.tts import TTS

# Initialize Pipeline
pipeline = TranslationPipeline()
stt = STT()
tts = TTS()

def process_text(text, target_lang, use_glossary):
    # TODO: Pass use_glossary flag to pipeline if needed, 
    # currently it's auto-applied but we could toggle it.
    output = pipeline.translate(text, target_lang=target_lang)
    
    # Format logs for display
    logs = output.get("logs", {})
    log_str = "Processing Steps:\n"
    for k, v in logs.items():
        log_str += f"- {k}: {v}\n"
        
    confidence_markup = f"Confidence: {output['confidence']:.2f}"
    if output['confidence'] < 0.5:
        confidence_markup += " ⚠️ (Low Confidence)"
        
    return output["translation"], log_str, confidence_markup

def process_audio(audio_path, target_lang):
    if not audio_path:
        return "", "No audio provided", "", None
        
    # STT
    transcription = stt.transcribe(audio_path)
    
    # Translation
    output = pipeline.translate(transcription, target_lang=target_lang)
    translation = output["translation"]
    
    # TTS
    audio_out_path = f"outputs/tts_output_{len(translation)}.mp3"
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
        
    final_audio = tts.speak(translation, lang=target_lang, output_file=audio_out_path)
    
    logs = output.get("logs", {})
    log_str = f"Transcription: {transcription}\n\nProcessing Steps:\n"
    for k, v in logs.items():
        log_str += f"- {k}: {v}\n"
        
    return transcription, translation, log_str, final_audio

# UI Layout
with gr.Blocks(title="BharatCodeMix") as app:
    gr.Markdown("# 🇮🇳 BharatCodeMix\n### Dialect & Code-Mixed Translation System")
    
    with gr.Tabs():
        # Tab 1: Text Translation
        with gr.TabItem("Text Translate"):
            with gr.Row():
                with gr.Column():
                    input_text = gr.Textbox(label="Input Text (English/Hinglish/Hindi)", placeholder="Type here... e.g. 'Main aaj bahut happy hoon'")
                    target_lang = gr.Dropdown(["Hindi", "English"], label="Target Language", value="Hindi")
                    use_glossary = gr.Checkbox(label="Apply Glossary Constraints", value=True)
                    btn_text = gr.Button("Translate", variant="primary")
                
                with gr.Column():
                    output_text = gr.Textbox(label="Translated Text")
                    confidence_display = gr.Text(label="Quality Check")
                    logs_display = gr.TextArea(label="Pipeline Logs", interactive=False)
            
            btn_text.click(process_text, inputs=[input_text, target_lang, use_glossary], outputs=[output_text, logs_display, confidence_display])
            
            gr.Examples(
                examples=[
                    ["Main aaj bahut happy hoon", "Hindi", True],
                    ["Exam ka tension mat le, bas chill kar", "Hindi", True],
                    ["Code-mix is quite difficult to handle.", "Hindi", True]
                ],
                inputs=[input_text, target_lang, use_glossary]
            )

        # Tab 2: Speech Translation
        with gr.TabItem("Speech Translate"):
            with gr.Row():
                with gr.Column():
                    input_audio = gr.Audio(sources=["upload"], type="filepath", label="Upload Audio")
                    target_lang_audio = gr.Dropdown(["Hindi", "English"], label="Target Language", value="Hindi")
                    btn_audio = gr.Button("Transcribe & Translate", variant="primary")
                    
                with gr.Column():
                    stt_output = gr.Textbox(label="Recognized Text")
                    trans_output = gr.Textbox(label="Translated Text")
                    logs_audio = gr.TextArea(label="Pipeline Logs")
                    audio_result = gr.Audio(label="Spoken Translation")
            
            btn_audio.click(process_audio, inputs=[input_audio, target_lang_audio], outputs=[stt_output, trans_output, logs_audio, audio_result])

        # Tab 3: Settings & Samples
        with gr.TabItem("Settings"):
            gr.Markdown("### Configuration")
            gr.Textbox(value="Local CPU Mode", label="Execution Mode", interactive=False)
            gr.Markdown("Edit `data/glossary_example.csv` to update glossary terms.")
            gr.Markdown("Edit `data/slang_map.json` to add new slang words.")

if __name__ == "__main__":
    app.launch()
