import os
from gtts import gTTS
import pyttsx3
import logging

logger = logging.getLogger(__name__)

class TTS:
    def __init__(self, use_online=True):
        self.use_online = use_online
        self.offline_engine = None
        if not use_online:
            self._init_offline()

    def _init_offline(self):
        try:
            self.offline_engine = pyttsx3.init()
        except Exception as e:
            logger.warning(f"Failed to init pyttsx3: {e}")

    def speak(self, text: str, lang: str = 'hi', output_file: str = "output.mp3") -> str:
        """Generates audio from text. Returns path to audio file."""
        if not text:
            return ""

        # Map typical lang codes to gTTS
        lang_map = {
            'Hindi': 'hi',
            'English': 'en',
            'Kannada': 'kn',
            'Marathi': 'mr'
        }
        target_lang = lang_map.get(lang, 'en')

        try:
            if self.use_online:
                tts = gTTS(text=text, lang=target_lang, slow=False)
                tts.save(output_file)
                return output_file
            else:
                if self.offline_engine:
                    # pyttsx3 is limited in language support out of box
                    self.offline_engine.save_to_file(text, output_file)
                    self.offline_engine.runAndWait()
                    return output_file
                else:
                    logger.error("No offline engine available")
                    return ""
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            return ""
