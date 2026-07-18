import re

# Phase 2 additions
SUBJECT_WORDS = [
    "subject",
    "topic",
    "about",
    "genre",
    "category",
    "field"
]

LANGUAGE_LIST = [
    "english", "spanish", "french", "arabic", "german",
    "chinese", "hindi", "portuguese", "russian", "japanese", "urdu"
]



TITLE_WORDS = [
    "find",
    "show",
    "search",
    "book",
    "books",
    "about"
]

AUTHOR_WORDS = [
    "author",
    "written by",
    "by"
]

DETAIL_WORDS = [
    "details",
    "detail",
    "information",
    "info"
]

TIME_WORDS = [
    "time",
    "timing",
    "hour",
    "hours",
    "open",
    "close"
]

MEMBERSHIP_WORDS = [
    "membership",
    "member",
    "join",
    "register"
]


def clean(text, words):

    result = text

    words = sorted(words, key=len, reverse=True)

    for w in words:
        result = result.replace(w, " ")

    return " ".join(result.split())


# --- Phase 2 helpers ---

def _extract_year(text):
    """Return 4-digit year string if found, else None."""
    m = re.search(r'\b(19|20)\d{2}\b', text)
    return m.group() if m else None


def _extract_language(text):
    """Return language name if an explicit language is mentioned."""
    for lang in LANGUAGE_LIST:
        if lang in text:
            return lang
    return None


def _build_filters(text):
    """
    Extract a dict of search dimensions from a combined query.
    Used when FILTER_SEARCH is detected.
    Returns only the dimensions that are actually found.
    """
    filters = {}

    year = _extract_year(text)
    if year:
        filters['year'] = year

    lang = _extract_language(text)
    if lang:
        filters['language'] = lang

    if 'publisher' in text:
        kw = clean(text.replace('publisher', ''), ['books', 'in', 'find', 'show', year or '', lang or ''])
        if kw:
            filters['publisher'] = kw

    if any(w in text for w in AUTHOR_WORDS):
        if 'written by' in text:
            kw = text.split('written by', 1)[-1]
        elif 'by ' in text:
            kw = text.split('by ', 1)[-1]
        elif 'author' in text:
            kw = text.replace('author', '')
        else:
            kw = ''
        kw = clean(kw, ['books', 'published', 'in', 'find', 'show', year or '', lang or ''])
        if kw:
            filters['author'] = kw

    for sw in SUBJECT_WORDS:
        if sw in text:
            kw = text.split(sw, 1)[-1]
            kw = clean(kw, ['books', 'in', 'find', 'show', 'search', year or '', lang or ''])
            if kw:
                filters['subject'] = kw
            break

    if 'branch' in text:
        kw = clean(text.replace('branch', ''), ['books', 'in', 'at', 'find', 'show', year or '', lang or ''])
        if kw:
            filters['branch'] = kw
    else:
        m = re.search(r'\bat\s+([a-z][a-z\s]+?)(?:\s+library)?\s*$', text)
        if m:
            filters['branch'] = m.group(1).strip()

    # General title keyword — only when no author/subject/publisher found
    if not any(k in filters for k in ['author', 'subject', 'publisher']):
        stop = ['books', 'book', 'find', 'show', 'search', 'published', 'in', 'at',
                year or '', lang or '']
        kw = clean(text, TITLE_WORDS + stop)
        if kw:
            filters['title'] = kw

    return {k: v for k, v in filters.items() if v}


def detect_intent(message):
    text = message.lower().strip()

    # Static intents — always checked first
    if any(w in text for w in TIME_WORDS):
        return ("TIMINGS", "")
    if any(w in text for w in MEMBERSHIP_WORDS):
        return ("MEMBERSHIP", "")

    # --- Phase 2: Filter combination detection ---
    # Count how many distinct search dimensions are present
    year = _extract_year(text)
    lang = _extract_language(text)
    has_author  = any(w in text for w in AUTHOR_WORDS)
    has_subject = any(w in text for w in SUBJECT_WORDS)
    has_branch  = 'branch' in text or bool(re.search(r'\bat\s+[a-z]', text))
    has_publisher = 'publisher' in text

    active_dims = sum([bool(year), bool(lang), has_author, has_subject, has_branch, has_publisher])

    if active_dims >= 2:
        filters = _build_filters(text)
        if len(filters) >= 2:
            return ("FILTER_SEARCH", filters)

    # --- Phase 2: Subject / topic search ---
    if has_subject and not has_author:
        for sw in SUBJECT_WORDS:
            if sw in text:
                # Extract keyword: text after the subject word, strip stop words
                kw = text.split(sw, 1)[-1].strip()
                # Use word-boundary regex to avoid corrupting words containing stop words
                stop_pattern = r'\b(?:books?|find|show|search)\b'
                kw = re.sub(stop_pattern, '', kw).strip()
                kw = ' '.join(kw.split())  # normalise spaces
                return ("SUBJECT_SEARCH", kw or clean(text, SUBJECT_WORDS + TITLE_WORDS))
    
    if "recommend" in text or "similar to" in text:
        keyword = clean(text, ["recommend", "books", "similar to", "like"])
        return ("RECOMMEND", keyword)
        
    if "publisher" in text:
        return ("PUBLISHER_SEARCH", text.replace("publisher", "").strip())
        
    if "branch" in text or "library" in text:
        keyword = clean(text, ["branch", "library", "in", "at"])
        return ("BRANCH_SEARCH", keyword)
        
    if "call number" in text:
        return ("CALLNUMBER_SEARCH", text.replace("call number", "").strip())
        
    if "language" in text or "in " in text:
        if "in english" in text or "in spanish" in text or "in french" in text:
            return ("LANGUAGE_SEARCH", text.split("in ")[-1].strip())
            
    if "year" in text or "published in" in text:
        year_match = re.search(r"\b(19|20)\d{2}\b", text)
        if year_match:
            return ("YEAR_SEARCH", year_match.group())

    isbn = re.search(r"\b\d{10,13}\b", text)
    if isbn:
        return ("ISBN_SEARCH", isbn.group())
        
    barcode = re.search(r"\b[a-zA-Z0-9]{5,15}\b", text)
    if "barcode" in text and barcode:
        return ("BARCODE_SEARCH", text.replace("barcode", "").strip())

    if "written by" in text or text.startswith("by "):
        keyword = clean(text, AUTHOR_WORDS)
        return ("AUTHOR_SEARCH", keyword)

    if any(w in text for w in DETAIL_WORDS):
        keyword = clean(text, DETAIL_WORDS)
        return ("DETAILS", keyword)

    keyword = clean(text, TITLE_WORDS)
    if keyword != "":
        return ("TITLE_SEARCH", keyword)

    return ("UNKNOWN", "")
