from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.formatter_service import render_books
from app.services.intent_service import detect_intent
from app.services.koha_service import search_by_publisher
from app.services.koha_service import (
    search_books,
    search_by_title,
    search_by_author,
    search_by_isbn,
)
from app.services.formatter_service import render_books

app = FastAPI(title="Koha OPAC AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
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
    elif intent=="PUBLISHER_SEARCH":

        books=search_by_publisher(keyword)
    else:
        books = search_books(keyword)

    if books:
        return {
            "response": render_books(books)
        }

    return {
        "response": f"""
<div class="empty-state">

<div class="empty-title">

No Books Found

</div>

<div class="empty-text">

No books matched "<b>{keyword}</b>".

Try another title, author, or ISBN.

</div>

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
