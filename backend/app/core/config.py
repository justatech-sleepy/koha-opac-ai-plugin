"""
core/config.py — Application settings loaded from .env
"""

from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    # -----------------------------------------------------------------------
    # Application
    # -----------------------------------------------------------------------
    APP_NAME:    str = os.getenv("APP_NAME", "Koha OPAC AI Assistant")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.1")
    DEBUG:       bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL:   str = os.getenv("LOG_LEVEL", "INFO")

    # -----------------------------------------------------------------------
    # CORS — comma-separated list of allowed origins
    # -----------------------------------------------------------------------
    _raw_origins: str = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:8081,http://localhost:8081")
    ALLOWED_ORIGINS: list[str] = (
        ["*"] if _raw_origins.strip() == "*"
        else [o.strip() for o in _raw_origins.split(",") if o.strip()]
    )

    # -----------------------------------------------------------------------
    # Database
    # -----------------------------------------------------------------------
    DB_HOST:     str = os.getenv("DB_HOST", "localhost")
    DB_PORT:     int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME:     str = os.getenv("DB_NAME", "")
    DB_USER:     str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    # -----------------------------------------------------------------------
    # Search
    # Supported: "auto" | "sql" | "zebra" | "elasticsearch"
    # -----------------------------------------------------------------------
    SEARCH_ENGINE:      str = os.getenv("SEARCH_ENGINE", "auto")
    ELASTICSEARCH_URL:  str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

    # -----------------------------------------------------------------------
    # LLM Settings
    # -----------------------------------------------------------------------
    LLM_PROVIDER:   str = os.getenv("LLM_PROVIDER", "openai")  # 'openai', 'gemini' or 'groq'
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL:   str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL:   str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")
    
    GROQ_API_KEY:   str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL:     str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    # -----------------------------------------------------------------------
    # Koha REST API (optional, for future use)
    # -----------------------------------------------------------------------
    KOHA_URL:          str = os.getenv("KOHA_URL", "http://localhost:8080")
    KOHA_API_URL:      str = os.getenv("KOHA_API_URL", "http://localhost:8081")
    KOHA_API_USER:     str = os.getenv("KOHA_API_USER", "")
    KOHA_API_PASSWORD: str = os.getenv("KOHA_API_PASSWORD", "")

    # -----------------------------------------------------------------------
    # Request timeout (seconds)
    # -----------------------------------------------------------------------
    TIMEOUT: int = int(os.getenv("TIMEOUT", "10"))


settings = Settings()
