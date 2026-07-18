"""
test_search.py — Unit tests for Phase 2 search functions.
Tests use mocking to avoid requiring a live database.
"""

import pytest
from unittest.mock import patch, MagicMock


# --- search_with_filters ---

@patch('app.services.koha_service.execute_search')
def test_filter_by_title_and_year(mock_exec):
    mock_exec.return_value = [{'biblionumber': 1, 'title': 'Python 2023', 'author': 'A', 'isbn': None,
                                'barcode': None, 'homebranch': 'Main', 'itemcallnumber': '001',
                                'availability': 'Available'}]
    from app.services.koha_service import search_with_filters
    results = search_with_filters({'title': 'Python', 'year': '2023'})
    assert mock_exec.called
    call_sql = mock_exec.call_args[0][0]
    assert "b.title LIKE %s" in call_sql
    assert "bi.publicationyear LIKE %s" in call_sql
    assert len(results) == 1


@patch('app.services.koha_service.execute_search')
def test_filter_by_author_and_language(mock_exec):
    mock_exec.return_value = []
    from app.services.koha_service import search_with_filters
    search_with_filters({'author': 'Matthes', 'language': 'french'})
    call_sql = mock_exec.call_args[0][0]
    assert "b.author LIKE %s" in call_sql
    assert "bm.metadata LIKE %s" in call_sql


@patch('app.services.koha_service.execute_search')
def test_filter_empty_dict_returns_empty(mock_exec):
    from app.services.koha_service import search_with_filters
    results = search_with_filters({})
    assert results == []
    mock_exec.assert_not_called()


@patch('app.services.koha_service.execute_search')
def test_filter_by_subject_and_branch(mock_exec):
    mock_exec.return_value = []
    from app.services.koha_service import search_with_filters
    search_with_filters({'subject': 'history', 'branch': 'Central'})
    call_sql = mock_exec.call_args[0][0]
    assert "bm.metadata LIKE %s" in call_sql
    assert "i.homebranch LIKE %s" in call_sql


# --- search_fuzzy ---

@patch('app.services.koha_service.execute_search')
def test_fuzzy_uses_soundex(mock_exec):
    mock_exec.return_value = [{'biblionumber': 2, 'title': 'Python', 'author': 'Matthes',
                                'isbn': None, 'barcode': None, 'homebranch': 'Main',
                                'itemcallnumber': '001', 'availability': 'Available'}]
    from app.services.koha_service import search_fuzzy
    results = search_fuzzy("Pyton")
    assert mock_exec.called
    call_sql = mock_exec.call_args[0][0]
    assert "SOUNDEX" in call_sql
    assert len(results) == 1


@patch('app.services.koha_service.execute_search')
def test_fuzzy_falls_back_to_like_on_no_results(mock_exec):
    # First call (SOUNDEX) returns empty; second call (LIKE) returns results
    mock_exec.side_effect = [
        [],  # SOUNDEX returns nothing
        [{'biblionumber': 3, 'title': 'Python Crash Course', 'author': 'Matthes',
          'isbn': None, 'barcode': None, 'homebranch': 'Main',
          'itemcallnumber': '001', 'availability': 'Available'}]
    ]
    from app.services.koha_service import search_fuzzy
    results = search_fuzzy("python crash")
    assert mock_exec.call_count == 2
    assert len(results) == 1
