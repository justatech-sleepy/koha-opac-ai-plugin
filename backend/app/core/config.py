from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "Koha OPAC AI Assistant")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "True") == "True"

    KOHA_URL = os.getenv("KOHA_URL", "http://localhost:8080")

    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))

settings = Settings()
