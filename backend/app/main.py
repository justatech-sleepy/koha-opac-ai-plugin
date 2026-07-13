from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from collections import defaultdict
import pymysql

from app.services.formatter_service import render_books
from app.services.intent_service import detect_intent
from app.services.koha_service import search_by_publisher
from app.services.koha_service import (
    search_books,
    search_by_title,
    search_by_author,
    search_by_isbn,
)

app = FastAPI(title="Koha OPAC AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rate Limiting ---
RATE_LIMIT_WINDOW = 60 # seconds
RATE_LIMIT_MAX_REQUESTS = 20
request_history = defaultdict(list)

class RateLimitExceeded(Exception):
    pass

def check_rate_limit(request: Request):
    ip = request.client.host
    now = time.time()
    history = [t for t in request_history[ip] if now - t < RATE_LIMIT_WINDOW]
    if len(history) >= RATE_LIMIT_MAX_REQUESTS:
        raise RateLimitExceeded()
    history.append(now)
    request_history[ip] = history

# --- Exception Handlers ---
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=200,
        content={
            "response": f"""
<div class="empty-state">
  <div class="empty-icon">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="24" height="24">
      <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
    </svg>
  </div>
  <div class="empty-title">Slow Down</div>
  <div class="empty-text">You are searching too fast. Please wait a moment and try again.</div>
</div>
"""
        }
    )

@app.exception_handler(pymysql.Error)
async def db_exception_handler(request: Request, exc: pymysql.Error):
    return JSONResponse(
        status_code=200,
        content={
            "response": f"""
<div class="empty-state">
  <div class="empty-icon">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="24" height="24">
      <circle cx="12" cy="12" r="10"/><path d="M8 12h.01"/><path d="M12 12h.01"/><path d="M16 12h.01"/>
    </svg>
  </div>
  <div class="empty-title">Service Unavailable</div>
  <div class="empty-text">The catalog is currently experiencing high load or undergoing maintenance. Please try again later.</div>
</div>
"""
        }
    )

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat", dependencies=[Depends(check_rate_limit)])
def chat(request: ChatRequest):

    intent, keyword = detect_intent(request.message)

    if intent == "TIMINGS":
        return {
            "response": """
<h3>Library Hours</h3>

<p>
Monday - Friday<br>
9:00 AM - 5:00 PM
</p>
"""
        }

    if intent == "MEMBERSHIP":
        return {
            "response": """
<h3>Library Membership</h3>

<p>
Bring your Student ID to register for library membership.
</p>
"""
        }

    if intent == "TITLE_SEARCH":
        books = search_by_title(keyword)
    elif intent == "AUTHOR_SEARCH":
        books = search_by_author(keyword)
    elif intent == "ISBN_SEARCH":
        books = search_by_isbn(keyword)
    elif intent == "PUBLISHER_SEARCH":
        books = search_by_publisher(keyword)
    elif intent == "BARCODE_SEARCH":
        from app.services.koha_service import search_by_barcode
        books = search_by_barcode(keyword)
    elif intent == "CALLNUMBER_SEARCH":
        from app.services.koha_service import search_by_callnumber
        books = search_by_callnumber(keyword)
    elif intent == "BRANCH_SEARCH":
        from app.services.koha_service import search_by_branch
        books = search_by_branch(keyword)
    elif intent == "LANGUAGE_SEARCH":
        from app.services.koha_service import search_by_language
        books = search_by_language(keyword)
    elif intent == "YEAR_SEARCH":
        from app.services.koha_service import search_by_year
        books = search_by_year(keyword)
    elif intent == "RECOMMEND":
        # simple recommendation: find same author or subject
        books = search_by_author(keyword)
        if not books:
            from app.services.koha_service import search_by_subject
            books = search_by_subject(keyword)
    else:
        books = search_books(keyword)

    if books:
        return {
            "response": render_books(books)
        }

    return {
        "response": f"""
<div class="empty-state">
  <div class="empty-icon">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="24" height="24">
      <circle cx="12" cy="12" r="10"/><path d="M8 12h.01"/><path d="M12 12h.01"/><path d="M16 12h.01"/>
    </svg>
  </div>
  <div class="empty-title">No books found</div>
  <div class="empty-text">Try another keyword or browse our suggestions.</div>
</div>
"""
    }


@app.get("/")
def root():
    return {
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/api/suggestions", dependencies=[Depends(check_rate_limit)])
def get_suggestions(q: str = ""):
    if not q or len(q) < 3:
        return {"suggestions": []}
    
    books = search_by_title(q)
    suggestions = list(set([book['title'] for book in books[:7]]))
    return {"suggestions": suggestions}

