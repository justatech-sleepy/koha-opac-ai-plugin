"""
routers/chat.py — Chat endpoint router
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, validator

from app.services.intent_service import detect_intent
from app.services.search_service import (
    search_books,
    search_by_title,
    search_by_author,
    search_by_isbn,
    search_by_publisher,
    search_by_barcode,
    search_by_callnumber,
    search_by_branch,
    search_by_language,
    search_by_year,
    search_by_subject,
    search_with_filters,
    search_fuzzy,
)
from app.services.formatter_service import render_books
from app.core.rate_limiter import check_rate_limit

router = APIRouter(prefix="/api", tags=["chat"])

# -----------------------------------------------------------------------
# Request / response models
# -----------------------------------------------------------------------


class ChatRequest(BaseModel):
    message: str

    @validator("message")
    def message_not_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("message must not be empty")
        if len(v) > 512:
            raise ValueError("message too long (max 512 characters)")
        return v


# -----------------------------------------------------------------------
# Static response helpers
# -----------------------------------------------------------------------

_TIMINGS_HTML = """
<h3>Library Hours</h3>
<p>Monday – Friday: 9:00 AM – 5:00 PM<br>
Saturday: 10:00 AM – 3:00 PM<br>
Sunday: Closed</p>
"""

_MEMBERSHIP_HTML = """
<h3>Library Membership</h3>
<p>Bring your Student or Staff ID to the main desk to register for a free library membership.</p>
"""

_NOT_FOUND_HTML = """
<div class="empty-state">
  <div class="empty-title">No books found</div>
  <div class="empty-text">Try another keyword, an ISBN, or browse our suggestions.</div>
</div>
"""


# -----------------------------------------------------------------------
# Chat endpoint
# -----------------------------------------------------------------------

@router.post("/chat", dependencies=[Depends(check_rate_limit)])
def chat(request: ChatRequest):
    intent, keyword = detect_intent(request.message)

    # --- Static intents ---
    if intent == "TIMINGS":
        return {"response": _TIMINGS_HTML}

    if intent == "MEMBERSHIP":
        return {"response": _MEMBERSHIP_HTML}

    # --- Search intents ---
    books = []

    search_map = {
        "TITLE_SEARCH": lambda k: search_by_title(k),
        "AUTHOR_SEARCH": lambda k: search_by_author(k),
        "ISBN_SEARCH": lambda k: search_by_isbn(k),
        "PUBLISHER_SEARCH": lambda k: search_by_publisher(k),
        "BARCODE_SEARCH": lambda k: search_by_barcode(k),
        "CALLNUMBER_SEARCH": lambda k: search_by_callnumber(k),
        "BRANCH_SEARCH": lambda k: search_by_branch(k),
        "LANGUAGE_SEARCH": lambda k: search_by_language(k),
        "YEAR_SEARCH": lambda k: search_by_year(k),
        "SUBJECT_SEARCH": lambda k: search_by_subject(k),
        "RECOMMEND": lambda k: search_by_author(k) or search_by_subject(k),
        "FILTER_SEARCH": lambda k: search_with_filters(k),
    }

    handler = search_map.get(intent)
    if handler:
        books = handler(keyword) or []
    else:
        books = search_books(keyword)

    # --- Fuzzy fallback ---
    if not books and intent not in ("TIMINGS", "MEMBERSHIP", "FILTER_SEARCH"):
        raw_keyword = keyword if isinstance(keyword, str) else request.message
        books = search_fuzzy(raw_keyword)

    if books:
        return {"response": render_books(books)}

    return {"response": _NOT_FOUND_HTML}


# -----------------------------------------------------------------------
# Suggestions endpoint
# -----------------------------------------------------------------------

@router.get("/suggestions", dependencies=[Depends(check_rate_limit)])
def get_suggestions(q: str = ""):
    if not q or len(q) < 3:
        return {"suggestions": []}
    books = search_by_title(q)
    suggestions = list(dict.fromkeys(b["title"] for b in books[:7]))
    return {"suggestions": suggestions}
