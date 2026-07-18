"""
zebra_service.py — Zebra/SRU Search Adapter (Issue #3)

Skeleton adapter with the same interface as koha_service.py.
Full implementation planned for Phase 2 (Advanced Search).

To activate: set SEARCH_ENGINE=zebra and KOHA_API_URL in your .env
"""

from app.core.config import settings


def _sru_search(query: str) -> list:
    """
    Placeholder: will query Koha's SRU/Zebra endpoint.
    KOHA_API_URL must be configured in .env
    """
    # TODO (Phase 2): Implement SRU query against settings.KOHA_API_URL
    return []


def search_books(keyword):
    return _sru_search(f"any={keyword}")

def search_by_title(keyword):
    return _sru_search(f"dc.title={keyword}")

def search_by_author(keyword):
    return _sru_search(f"dc.author={keyword}")

def search_by_isbn(keyword):
    return _sru_search(f"bath.isbn={keyword}")

def search_by_publisher(keyword):
    return _sru_search(f"dc.publisher={keyword}")

def search_by_barcode(keyword):
    return _sru_search(f"barcode={keyword}")

def search_by_callnumber(keyword):
    return _sru_search(f"local.callnumber={keyword}")

def search_by_branch(keyword):
    return _sru_search(f"local.branch={keyword}")

def search_by_language(keyword):
    return _sru_search(f"dc.language={keyword}")

def search_by_year(keyword):
    return _sru_search(f"dc.date={keyword}")

def search_by_subject(keyword):
    return _sru_search(f"dc.subject={keyword}")
