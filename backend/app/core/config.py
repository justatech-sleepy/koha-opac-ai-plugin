from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME")
    APP_VERSION = os.getenv("APP_VERSION")
    DEBUG = os.getenv("DEBUG") == "True"

    KOHA_URL = os.getenv("KOHA_URL")

    LLM_PROVIDER = os.getenv("LLM_PROVIDER")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OLLAMA_URL = os.getenv("OLLAMA_URL")

settings = Settings()
