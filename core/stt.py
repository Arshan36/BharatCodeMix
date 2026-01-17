from faster_whisper import WhisperModel
import os
import logging

logger = logging.getLogger(__name__)

class STT:
    def __init__(self, model_size="tiny", device="cpu", compute_type="int8"):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None

    def load_model(self):
        if self.model is None:
            logger.info(f"Loading Whisper model: {self.model_size} on {self.device}")
            try:
                self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}")
                raise

    def transcribe(self, audio_path: str) -> str:
        """Transcribes audio file to text."""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        self.load_model()
        
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        logger.info(f"Detected language '{info.language}' with probability {info.language_probability}")

        full_text = ""
        for segment in segments:
            full_text += segment.text + " "
            
        return full_text.strip()
