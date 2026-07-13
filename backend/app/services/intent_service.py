import re


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


def detect_intent(message):
    text = message.lower().strip()
    
    if any(w in text for w in TIME_WORDS):
        return ("TIMINGS", "")
    if any(w in text for w in MEMBERSHIP_WORDS):
        return ("MEMBERSHIP", "")
    
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
