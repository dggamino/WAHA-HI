"""
Knowledge Adapter

Punto único de acceso entre Companion
y Knowledge Layer.
"""


from knowledge.books.catalog import catalog


def get_books():

    return catalog()


def find_book(book_id):

    books = get_books()

    for book in books:

        if book["id"] == book_id:
            return book

    return None
