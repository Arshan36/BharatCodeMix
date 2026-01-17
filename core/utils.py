import logging
import os
from dotenv import load_dotenv

def setup_logger(name="BharatCodeMix"):
    """Configures and returns a logger instance."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log", encoding='utf-8')
        ]
    )
    return logging.getLogger(name)

def load_config():
    """Loads environment variables and returns a config dictionary."""
    load_dotenv()
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "USE_GPU": os.getenv("USE_GPU", "False").lower() == "true",
        "DEFAULT_MODEL_EN_HI": "Helsinki-NLP/opus-mt-en-hi",
        "DEFAULT_MODEL_HI_EN": "Helsinki-NLP/opus-mt-hi-en",
    }
