def book_cover(isbn):
    if not isbn:
        return "https://placehold.co/120x180?text=No+Cover"
    isbn = isbn.replace("-", "").strip()
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"

def render_books(books):
    if not books:
        return ""

    # Group books by biblionumber
    grouped_books = {}
    for b in books:
        bib = b.get('biblionumber')
        if bib not in grouped_books:
            grouped_books[bib] = {
                'title': b.get('title', 'Unknown Title'),
                'author': b.get('author', 'Unknown Author'),
                'isbn': b.get('isbn'),
                'items': []
            }
        grouped_books[bib]['items'].append(b)

    html = f"<h3>Search Results ({len(grouped_books)})</h3><div class='books-container'>"

    for bib, data in grouped_books.items():
        cover = book_cover(data['isbn'])
        items = data['items']
        
        total_copies = len(items)
        available_copies = sum(1 for i in items if i.get('availability', '').lower() == 'available')
        
        # Get unique branches and call numbers
        branches = list(set([i.get('homebranch') for i in items if i.get('homebranch')]))
        call_numbers = list(set([i.get('itemcallnumber') for i in items if i.get('itemcallnumber')]))
        
        branch_text = ", ".join(branches) if branches else "N/A"
        call_text = ", ".join(call_numbers) if call_numbers else "N/A"

        import html
        safe_title = html.escape(str(data['title']))
        safe_author = html.escape(str(data['author']))
        safe_branch = html.escape(str(branch_text))
        safe_call = html.escape(str(call_text))

        color = "#10B981" if available_copies > 0 else "#EF4444"
        status_text = "Available" if available_copies > 0 else "Checked Out"

        html += f"""
<div class="book-card" tabindex="0">
    <div class="book-header">
        <div class="book-cover">
            <img src="{cover}" loading="lazy" onerror="this.src='https://placehold.co/120x180?text=Book';">
        </div>
        <div class="book-info">
            <div class="book-title">{safe_title}</div>
            <div class="book-author">{safe_author}</div>
            <div class="book-meta">
                <span class="badge" style="background:{color};color:white;width:max-content;margin-bottom:6px;">
                    {status_text}
                </span>
                <div class="meta-row"><strong>Branch:</strong> <span>{safe_branch}</span></div>
                <div class="meta-row"><strong>Copies:</strong> <span>{available_copies} of {total_copies}</span></div>
                <div class="meta-row"><strong>Shelf:</strong> <span>{safe_call}</span></div>
            </div>
        </div>
    </div>
    <div class="book-divider"></div>
    <div class="result-actions">
        <button class="result-btn secondary" tabindex="0">View Details</button>
        <button class="result-btn" disabled tabindex="-1" style="opacity:0.5; cursor:not-allowed;" title="Future Feature">Reserve</button>
    </div>
</div>
"""
    html += "</div>"
    return html
