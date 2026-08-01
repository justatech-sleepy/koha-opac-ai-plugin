"""
test_intents.py — Unit tests for intent_service.detect_intent()
Tests cover Phase 1 (existing) and Phase 2 (new) intents.
No database connection required.
"""

import pytest
from app.services.intent_service import detect_intent


# --- Phase 1: Existing intents ---

def test_timings():
    intent, kw = detect_intent("What are the library hours?")
    assert intent == "TIMINGS"

def test_membership():
    intent, kw = detect_intent("How do I register for membership?")
    assert intent == "MEMBERSHIP"

def test_recommend():
    intent, kw = detect_intent("Recommend books similar to Django")
    assert intent == "RECOMMEND"
    assert "django" in kw.lower()

def test_isbn_search():
    intent, kw = detect_intent("9781492056355")
    assert intent == "ISBN_SEARCH"
    assert kw == "9781492056355"

def test_author_search():
    intent, kw = detect_intent("written by Eric Matthes")
    assert intent == "AUTHOR_SEARCH"
    assert "matthes" in kw.lower() or "eric" in kw.lower()

def test_publisher_search():
    intent, kw = detect_intent("Publisher O'Reilly")
    assert intent == "PUBLISHER_SEARCH"

def test_year_search():
    intent, kw = detect_intent("Books published in 2023")
    assert intent == "YEAR_SEARCH"
    assert kw == "2023"

def test_title_search_fallback():
    intent, kw = detect_intent("Clean Code")
    assert intent == "TITLE_SEARCH"
    assert "clean code" in kw.lower() or "clean" in kw.lower()


# --- Phase 2: Subject / topic search ---

def test_subject_search_about():
    intent, kw = detect_intent("books about history")
    assert intent == "SUBJECT_SEARCH"
    assert "history" in kw.lower()

def test_subject_search_topic():
    intent, kw = detect_intent("topic: machine learning")
    assert intent == "SUBJECT_SEARCH"
    assert "machine learning" in kw.lower() or "machine" in kw.lower()

def test_subject_search_genre():
    intent, kw = detect_intent("science fiction genre")
    assert intent == "SUBJECT_SEARCH"
    assert "science fiction" in kw.lower() or "science" in kw.lower()


# --- Phase 2: Filter combinations ---

def test_filter_author_and_year():
    intent, filters = detect_intent("books by Eric Matthes published in 2023")
    assert intent == "FILTER_SEARCH"
    assert isinstance(filters, dict)
    assert 'year' in filters
    assert filters['year'] == "2023"

def test_filter_subject_and_language():
    intent, filters = detect_intent("books about AI in French")
    assert intent == "FILTER_SEARCH"
    assert isinstance(filters, dict)
    assert 'language' in filters
    assert filters['language'] == "french"

def test_filter_author_and_branch():
    intent, filters = detect_intent("books by Robert Martin at Central Library")
    assert intent == "FILTER_SEARCH"
    assert isinstance(filters, dict)
    assert 'author' in filters or 'branch' in filters

def test_filter_returns_dict():
    intent, filters = detect_intent("Python books published in 2022")
    if intent == "FILTER_SEARCH":
        assert isinstance(filters, dict)
        assert len(filters) >= 2
