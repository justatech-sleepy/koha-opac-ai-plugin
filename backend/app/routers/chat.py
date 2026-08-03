"""
routers/chat.py — Chat endpoint router
"""

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, validator
import html

from typing import List, Dict, Any, Optional

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
from app.llm.llm_service import generate_chat_response

router = APIRouter(prefix="/api", tags=["chat"])

# -----------------------------------------------------------------------
# Request / response models
# -----------------------------------------------------------------------

class MessageHistory(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[MessageHistory] = []

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
    # Combine history with the current message
    messages = [{"role": msg.role, "content": msg.content} for msg in request.history]
    messages.append({"role": "user", "content": request.message})
    
    # Process through LLM
    llm_response = generate_chat_response(messages)
    
    action = llm_response.get("action")
    data = llm_response.get("data")
    text_response = llm_response.get("text", "")
    
    escaped_text = html.escape(text_response).replace("\n", "<br>")
    final_html = f"<div class='chat-message-text'>{escaped_text}</div>"
    
    if action == "books":
        if data and len(data) > 0:
            final_html += render_books(data)
        else:
            final_html += _NOT_FOUND_HTML
    elif action == "timings":
        final_html += _TIMINGS_HTML
    elif action == "membership":
        final_html += _MEMBERSHIP_HTML
        
    return {
        "response": final_html,
        "raw_text": text_response
    }


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
