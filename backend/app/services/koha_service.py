from app.services.database import get_connection


def execute_search(sql, params):

    conn = get_connection()

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


def search_by_title(keyword):

    sql = BASE_QUERY + """
    WHERE b.title LIKE %s
    ORDER BY b.title
    LIMIT 20
    """

    return execute_search(sql, (f"%{keyword}%",))


def search_by_author(keyword):

    sql = BASE_QUERY + """
    WHERE b.author LIKE %s
    ORDER BY b.title
    LIMIT 20
    """

    return execute_search(sql, (f"%{keyword}%",))


def search_by_isbn(keyword):

    sql = BASE_QUERY + """
    WHERE bi.isbn LIKE %s
    LIMIT 20
    """

    return execute_search(sql, (f"%{keyword}%",))

def search_by_publisher(keyword):

    conn = get_connection()

    with conn.cursor() as cursor:

        sql = """

        SELECT

            b.biblionumber,

            b.title,

            b.author,

            bi.isbn,

            bi.publishercode,

            i.barcode,

            i.homebranch,

            i.itemcallnumber,

            CASE

                WHEN i.onloan IS NULL THEN 'Available'

                ELSE 'Checked Out'

            END availability

        FROM biblio b

        LEFT JOIN biblioitems bi

        ON b.biblionumber=bi.biblionumber

        LEFT JOIN items i

        ON b.biblionumber=i.biblionumber

        WHERE bi.publishercode LIKE %s

        LIMIT 10

        """

        search=f"%{keyword}%"

        cursor.execute(sql,(search,))

        return cursor.fetchall()
def search_by_subject(keyword):

    sql = BASE_QUERY + """
    WHERE bm.metadata LIKE %s
    LIMIT 20
    """

    return execute_search(sql, (f"%{keyword}%",))


def search_books(keyword):

    books = search_by_title(keyword)

    if books:
        return books

    books = search_by_author(keyword)

    if books:
        return books

    books = search_by_isbn(keyword)

    if books:
        return books

    books = search_by_subject(keyword)

    return books
