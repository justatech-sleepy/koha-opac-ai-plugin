"""
routers/vision.py — Book cover / barcode image scanning endpoint.

Accepts a base64 image, sends it to the configured LLM vision API,
and returns extracted book title / author / ISBN text.
"""

import os
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from openai import OpenAI

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["vision"])

# -----------------------------------------------------------------------
# Vision-capable model selection
# Priority:
#   1. Gemini  — gemini-1.5-flash (free, natively multimodal, best quality)
#   2. OpenAI  — gpt-4o-mini     (paid, vision support)
#   3. Groq    — llama-3.2-11b-vision-preview (set GROQ_VISION_MODEL in .env)
#
# When Groq is the main LLM provider but has no vision model on the account,
# we automatically fall back to Gemini if GEMINI_API_KEY is set in .env.
# -----------------------------------------------------------------------

_PROVIDER = settings.LLM_PROVIDER.lower()

if _PROVIDER == "gemini":
    _vision_client = OpenAI(
        api_key=settings.GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    _vision_model = settings.GEMINI_MODEL  # gemini-1.5-flash supports vision natively

elif _PROVIDER == "groq":
    groq_vision_model = os.getenv("GROQ_VISION_MODEL", "")
    if groq_vision_model:
        # Explicit override — use Groq with the specified vision model
        _vision_client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )
        _vision_model = groq_vision_model
        logger.info("Vision: using Groq model %s", _vision_model)
    elif settings.GEMINI_API_KEY:
        # Groq free tier often lacks vision models — fall back to Gemini for vision
        logger.info("Vision: Groq has no GROQ_VISION_MODEL set; falling back to Gemini.")
        _vision_client = OpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        _vision_model = settings.GEMINI_MODEL
    else:
        # Last resort: try Groq with the standard vision model
        _vision_client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )
        _vision_model = "llama-3.2-11b-vision-preview"
        logger.warning("Vision: no GROQ_VISION_MODEL or GEMINI_API_KEY; trying %s", _vision_model)

else:
    # OpenAI — gpt-4o-mini and gpt-4o both support vision
    _vision_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    _vision_model = settings.OPENAI_MODEL


# -----------------------------------------------------------------------
# Request model
# -----------------------------------------------------------------------

class VisionRequest(BaseModel):
    image: str  # full base64 data URL, e.g. "data:image/jpeg;base64,/9j/..."


# -----------------------------------------------------------------------
# Prompt
# -----------------------------------------------------------------------

VISION_PROMPT = (
    "You are a library assistant scanning an image. "
    "If the image shows a book cover, a barcode, or any printed library material: "
    "extract and return ONLY the book title, author name, ISBN, or barcode value — "
    "whichever is most clearly visible. Do NOT add any explanation or formatting. "
    "If the image does NOT contain any book, barcode, or library item at all, "
    "reply with exactly: NOT_A_BOOK"
)


# -----------------------------------------------------------------------
# Endpoint
# -----------------------------------------------------------------------

@router.post("/vision")
async def scan_image(req: VisionRequest):
    """
    Accepts a base64 data URL image and returns extracted book/barcode text.
    Response: {"text": "Hands-On Machine Learning ...", "not_a_book": false}
    """
    if not req.image or not req.image.startswith("data:image"):
        raise HTTPException(status_code=400, detail="Invalid image data. Must be a base64 data URL.")

    if len(req.image) > 5_000_000:
        raise HTTPException(status_code=413, detail="Image too large. Please use an image under 4 MB.")

    try:
        response = _vision_client.chat.completions.create(
            model=_vision_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": VISION_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": req.image,
                                "detail": "low",  # faster + cheaper; enough for book text
                            },
                        },
                    ],
                }
            ],
            max_tokens=150,
            temperature=0.0,
        )

        extracted = (response.choices[0].message.content or "").strip()
        logger.info("Vision result: %r  model=%s", extracted[:80], _vision_model)

        return {
            "text": extracted,
            "not_a_book": extracted.upper() == "NOT_A_BOOK",
        }

    except Exception as exc:
        logger.error("Vision endpoint error: %s", exc)
        raise HTTPException(status_code=500, detail=f"Vision AI error: {exc}")
