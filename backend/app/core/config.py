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
    _raw_origins: str = os.getenv("ALLOWED_ORIGINS", "*")
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
