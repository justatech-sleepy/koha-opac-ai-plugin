"""
routers/search.py — Book search, availability, and browsing endpoints
"""

from fastapi import APIRouter, Depends, Query
from app.services.search_service import (
    search_books,
    search_by_title,
    search_by_author,
    search_by_isbn,
    search_by_subject,
)
from app.core.rate_limiter import check_rate_limit

router = APIRouter(prefix="/api", tags=["search"])


@router.get("/search", dependencies=[Depends(check_rate_limit)])
def search(q: str = Query(...,
                          min_length=1,
                          max_length=256,
                          description="Search keyword"),
           field: str = Query("all",
                              description="Field to search: all | title | author | isbn | subject"),
           ):
    """
    General search endpoint. Returns raw book list (not rendered HTML).
    Frontend may use this for autocomplete or direct API consumers.
    """
    handlers = {
        "title": search_by_title,
        "author": search_by_author,
        "isbn": search_by_isbn,
        "subject": search_by_subject,
        "all": search_books,
    }
    fn = handlers.get(field, search_books)
    return {"results": fn(q), "count": 0, "query": q}


@router.get("/books", dependencies=[Depends(check_rate_limit)])
def books(
    q: str = Query("", max_length=256),
    limit: int = Query(20, ge=1, le=100),
):
    """Browse / list books matching an optional keyword."""
    results = search_books(q) if q else []
    return {"books": results[:limit], "total": len(results)}


@router.get("/availability")
def availability(isbn: str = Query(..., min_length=10,
                                   max_length=13, description="ISBN-10 or ISBN-13"), ):
    """Check availability of a specific item by ISBN."""
    results = search_by_isbn(isbn)
    if not results:
        return {"isbn": isbn, "available": False, "items": []}

    items = [
        {
            "biblionumber": r.get("biblionumber"),
            "title": r.get("title"),
            "branch": r.get("homebranch"),
            "callnumber": r.get("itemcallnumber"),
            "status": r.get("availability", "Unknown"),
        }
        for r in results
    ]
    available_count = sum(1 for i in items if i["status"] == "Available")
    return {
        "isbn": isbn,
        "available": available_count > 0,
        "available_count": available_count,
        "items": items,
    }
