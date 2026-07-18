"""
elasticsearch_service.py — Elasticsearch Search Adapter (Issue #3)

Skeleton adapter with the same interface as koha_service.py.
Full implementation planned for Phase 3 (AI & Recommendations).

To activate: set SEARCH_ENGINE=elasticsearch and ELASTICSEARCH_URL in your .env
"""

from app.core.config import settings


def _es_search(field: str, keyword: str) -> list:
    """
    Placeholder: will query Elasticsearch using the Python client.
    ELASTICSEARCH_URL must be configured in .env
    """
    # TODO (Phase 3): Implement using elasticsearch-py client
    # from elasticsearch import Elasticsearch
    # es = Elasticsearch(settings.ELASTICSEARCH_URL)
    # result = es.search(index="koha", query={"match": {field: keyword}})
    # return result["hits"]["hits"]
    return []


def search_books(keyword):
    return _es_search("_all", keyword)

def search_by_title(keyword):
    return _es_search("title", keyword)

def search_by_author(keyword):
    return _es_search("author", keyword)

def search_by_isbn(keyword):
    return _es_search("isbn", keyword)

def search_by_publisher(keyword):
    return _es_search("publisher", keyword)

def search_by_barcode(keyword):
    return _es_search("barcode", keyword)

def search_by_callnumber(keyword):
    return _es_search("itemcallnumber", keyword)

def search_by_branch(keyword):
    return _es_search("homebranch", keyword)

def search_by_language(keyword):
    return _es_search("language", keyword)

def search_by_year(keyword):
    return _es_search("copyrightdate", keyword)

def search_by_subject(keyword):
    return _es_search("subject", keyword)
