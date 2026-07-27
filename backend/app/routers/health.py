"""
routers/health.py — Health check and plugin config endpoints
"""

from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    """Liveness probe — returns 200 if the service is running."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app": settings.APP_NAME,
    }


@router.get("/")
def root():
    """Root endpoint — quick sanity check."""
    return {"status": "running", "version": settings.APP_VERSION}


@router.get("/api/config")
def config():
    """
    Returns safe, non-sensitive configuration values for the frontend.
    Never expose database credentials or secret keys here.
    """
    return {
        "search_engine": settings.SEARCH_ENGINE,
        "debug": settings.DEBUG,
        "version": settings.APP_VERSION,
    }


@router.get("/api/faq")
def faq():
    """Returns static FAQ entries for the chatbot."""
    return {
        "faqs": [
            {
                "question": "What are the library hours?",
                "answer": "Monday – Friday: 9:00 AM – 5:00 PM. Saturday: 10:00 AM – 3:00 PM. Sunday: Closed.",
            },
            {
                "question": "How do I register for a library membership?",
                "answer": "Bring your Student or Staff ID to the main desk to register for a free membership.",
            },
            {
                "question": "How do I renew a book?",
                "answer": "You can renew books online via the library catalogue, by phone, or in person at the desk.",
            },
        ]
    }
