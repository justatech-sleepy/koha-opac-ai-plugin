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
    if "publisher" in text:
        keyword=text.replace("publisher","").strip()
        return "PUBLISHER_SEARCH",keyword
    if any(w in text for w in MEMBERSHIP_WORDS):
        return ("MEMBERSHIP", "")

    isbn = re.search(r"\b\d{10,13}\b", text)

    if isbn:
        return ("ISBN_SEARCH", isbn.group())

    if "written by" in text:

        keyword = clean(text, AUTHOR_WORDS)

        return ("AUTHOR_SEARCH", keyword)

    if text.startswith("by "):

        keyword = clean(text, AUTHOR_WORDS)

        return ("AUTHOR_SEARCH", keyword)

    if any(w in text for w in DETAIL_WORDS):

        keyword = clean(text, DETAIL_WORDS)

        return ("DETAILS", keyword)

    keyword = clean(text, TITLE_WORDS)

    if keyword != "":
        return ("TITLE_SEARCH", keyword)

    return ("UNKNOWN", "")
