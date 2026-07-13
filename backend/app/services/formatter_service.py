def book_cover(isbn):

    if not isbn:
        return "https://placehold.co/120x180?text=No+Cover"

    isbn = isbn.replace("-", "").strip()

    return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"


def render_books(books):

    html = f"<h3>Search Results ({len(books)})</h3>"

    for book in books:

        cover = book_cover(book.get("isbn"))

        status = book.get("availability", "Unknown")

        color = "#10B981"

        if status.lower() != "available":
            color = "#EF4444"

        html += f"""

<div class="book-card">

<div class="book-header">

<div class="book-cover">

<img
src="{cover}"
onerror="this.src='https://placehold.co/120x180?text=Book';">

</div>

<div style="flex:1;">

<div class="book-title">

{book['title']}

</div>

<div class="book-author">

{book['author']}

</div>

<div class="book-meta">

<strong>ISBN</strong>

<span>{book.get('isbn') or 'N/A'}</span>

<strong>Barcode</strong>

<span>{book.get('barcode') or 'N/A'}</span>

<strong>Branch</strong>

<span>{book.get('homebranch') or 'N/A'}</span>

<strong>Call No</strong>

<span>{book.get('itemcallnumber') or 'N/A'}</span>

</div>

<div class="status-bar">

<span
class="badge available"
style="background:{color};color:white;">

{status}

</span>

</div>

</div>

</div>

</div>

"""

    return html
