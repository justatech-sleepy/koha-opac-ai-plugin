"""
search_service.py — Search Router (Issue #3)

This is the single entry point for all search operations.
It reads SEARCH_ENGINE from config and delegates to the correct adapter:
  - "sql" or "auto" (no other engine configured) → koha_service (SQL/MariaDB)
  - "zebra"         → zebra_service (Zebra/SRU)
  - "elasticsearch" → elasticsearch_service (Elasticsearch)

The rest of the project only imports from here — adapters are internal.
"""

from app.core.config import settings


def _get_adapter():
    engine = settings.SEARCH_ENGINE.lower()

    if engine == "elasticsearch":
        from app.services import elasticsearch_service as adapter
    elif engine == "zebra":
        from app.services import zebra_service as adapter
    else:
        # "auto" falls back to SQL (default, always available)
        from app.services import koha_service as adapter

    return adapter


def search_books(keyword):
    return _get_adapter().search_books(keyword)

def search_by_title(keyword):
    return _get_adapter().search_by_title(keyword)

def search_by_author(keyword):
    return _get_adapter().search_by_author(keyword)

def search_by_isbn(keyword):
    return _get_adapter().search_by_isbn(keyword)

def search_by_publisher(keyword):
    return _get_adapter().search_by_publisher(keyword)

def search_by_barcode(keyword):
    return _get_adapter().search_by_barcode(keyword)

def search_by_callnumber(keyword):
    return _get_adapter().search_by_callnumber(keyword)

def search_by_branch(keyword):
    return _get_adapter().search_by_branch(keyword)

def search_by_language(keyword):
    return _get_adapter().search_by_language(keyword)

def search_by_year(keyword):
    return _get_adapter().search_by_year(keyword)

def search_by_subject(keyword):
    return _get_adapter().search_by_subject(keyword)

# --- Phase 2 ---

def search_with_filters(filters: dict):
    return _get_adapter().search_with_filters(filters)

def search_fuzzy(keyword: str):
    return _get_adapter().search_fuzzy(keyword)
