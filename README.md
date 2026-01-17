# BharatCodeMix: Dialect & Code-Mixed Translation System

BharatCodeMix is a robust, local-first translation system designed specifically for Indian languages, handling code-mixing (Hinglish), dialects, and transliteration challenges that mainstream translators often miss.

## Features

- **Code-Mixed Translation**: Handles Hinglish (Hindi-English mixed) text seamlessly.
- **Dialect & Slang Normalization**: Understands "bindass", "jugaad" and maps them to formal Hindi/English.
- **Transliteration**: Converts Romanized Hindi (e.g., "kya haal hai") to Devanagari before translation.
- **Speech Support**: Speech-to-Text (STT) and Text-to-Speech (TTS) for end-to-end audio translation.
- **Quality Verification**: Auto-estimates translation quality and flags low-confidence results.
- **Local Privacy**: Runs entirely on your CPU using open-source models (HuggingFace Transformers).

## Quickstart

### Prerequisites
- Python 3.9+ installed
- valid internet connection (for first-time model download)

### Installation

1. Clone or unzip this repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: For audio support, you might need ffmpeg installed on your system.*

### Running the App

```bash
python run_app.py
```
Open your browser to the local Gradio URL (usually `http://127.0.0.1:7860`).

## Architecture

- **Core Pipeline**: `core/pipeline.py` orchestrates the flow.
- **Normalization**: `core/normalize.py` handles slang and script conversion.
- **Models**: Uses `Helsinki-NLP/opus-mt` for translation and `faster-whisper` for STT.

## Troubleshooting

- **Model Download Failed**: Ensure you have internet access. Large models might timeout on slow connections.
- **Audio Error**: Install `ffmpeg` and add it to your PATH.
- **Slow Performance**: This runs on CPU by default. STT and Translation can be slow on older machines.

## License

MIT
