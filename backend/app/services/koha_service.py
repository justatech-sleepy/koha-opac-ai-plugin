from app.core.database import get_db_connection

def execute_search(sql, params):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

BASE_QUERY = """
SELECT DISTINCT
    b.biblionumber,
    b.title,
    b.author,
    bi.isbn,
    i.barcode,
    i.homebranch,
    i.itemcallnumber,
    CASE
        WHEN i.onloan IS NULL THEN 'Available'
        ELSE 'Checked Out'
    END AS availability
FROM biblio b
LEFT JOIN biblioitems bi
    ON bi.biblionumber=b.biblionumber
LEFT JOIN items i
    ON i.biblionumber=b.biblionumber
LEFT JOIN biblio_metadata bm
    ON bm.biblionumber=b.biblionumber
"""

def search_books(keyword):
    """
    Optimized single query to search across title, author, isbn, barcode, and subject
    simultaneously, rather than N+1 waterfall queries.
    """
    sql = BASE_QUERY + """
    WHERE b.title LIKE %s
       OR b.author LIKE %s
       OR bi.isbn LIKE %s
       OR i.barcode = %s
       OR bm.metadata LIKE %s
    ORDER BY 
        CASE 
            WHEN b.title LIKE %s THEN 1 
            WHEN b.author LIKE %s THEN 2 
            ELSE 3 
        END,
        b.title
    LIMIT 30
    """
    
    like_keyword = f"%{keyword}%"
    params = (
        like_keyword,      # b.title
        like_keyword,      # b.author
        like_keyword,      # bi.isbn
        keyword,           # i.barcode (exact match)
        like_keyword,      # bm.metadata (subject/language)
        
        # ORDER BY weights
        like_keyword,      # weight title
        like_keyword       # weight author
    )
    
    return execute_search(sql, params)

def search_by_publisher(keyword):
    sql = BASE_QUERY + " WHERE bi.publishercode LIKE %s LIMIT 10"
    return execute_search(sql, (f"%{keyword}%",))

def search_by_title(keyword):
    sql = BASE_QUERY + " WHERE b.title LIKE %s LIMIT 10"
    return execute_search(sql, (f"%{keyword}%",))

def search_by_author(keyword):
    sql = BASE_QUERY + " WHERE b.author LIKE %s LIMIT 10"
    return execute_search(sql, (f"%{keyword}%",))

def search_by_isbn(keyword):
    sql = BASE_QUERY + " WHERE bi.isbn LIKE %s LIMIT 10"
    return execute_search(sql, (f"%{keyword}%",))

def search_by_barcode(keyword):
    sql = BASE_QUERY + " WHERE i.barcode = %s LIMIT 10"
    return execute_search(sql, (keyword,))

def search_by_callnumber(keyword):
    sql = BASE_QUERY + " WHERE i.itemcallnumber LIKE %s LIMIT 10"
    return execute_search(sql, (f"%{keyword}%",))

def search_by_branch(keyword):
    sql = BASE_QUERY + " WHERE i.homebranch LIKE %s LIMIT 10"
    return execute_search(sql, (f"%{keyword}%",))

def search_by_language(keyword):
    sql = BASE_QUERY + " WHERE bm.metadata LIKE %s LIMIT 10"
    return execute_search(sql, (f"%{keyword}%",))

def search_by_year(keyword):
    sql = BASE_QUERY + " WHERE bi.publicationyear LIKE %s LIMIT 10"
    return execute_search(sql, (f"%{keyword}%",))

def search_by_subject(keyword):
    sql = BASE_QUERY + " WHERE bm.metadata LIKE %s LIMIT 10"
    return execute_search(sql, (f"%{keyword}%",))

