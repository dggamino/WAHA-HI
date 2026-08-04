from dataclasses import dataclass


@dataclass
class Book:

    id: str
    title: str
    category: str
    status: str


BOOKS = [

    Book(
        id="HER-BOOK-001",
        title="Libro Fundacional HEREDITARIA",
        category="patrimonio familiar",
        status="development"
    ),

    Book(
        id="HER-BOOK-002",
        title="Libro del Cuidador",
        category="cuidado y evidencia",
        status="planned"
    ),

    Book(
        id="HER-BOOK-003",
        title="Libro del Patrimonio Invisible",
        category="activos familiares",
        status="planned"
    ),

    Book(
        id="HER-BOOK-004",
        title="Libro de la Memoria Familiar",
        category="historia patrimonial",
        status="planned"
    ),

    Book(
        id="HER-BOOK-005",
        title="Libro del Observatorio Familiar",
        category="datos y análisis",
        status="planned"
    ),

    Book(
        id="HER-BOOK-006",
        title="Libro del Futuro Hereditario",
        category="visión estratégica",
        status="planned"
    )

]


def list_books():

    return BOOKS


def get_book(book_id):

    for book in BOOKS:

        if book.id == book_id:
            return book

    return None
