"""
BooksFlow Foundation v0.1.0
"""

from ..base import BaseFlow


BOOKS = [
    {
        "id": "HER-BOOK-001",
        "title": "Libro Fundacional HEREDITARIA"
    },
    {
        "id": "HER-BOOK-002",
        "title": "Libro del Cuidador"
    },
    {
        "id": "HER-BOOK-003",
        "title": "Libro del Patrimonio Invisible"
    }
]


class BooksFlow(BaseFlow):

    name = "books"

    def execute(self, context):

        return {
            "status": "success",
            "flow": self.name,
            "books": BOOKS
        }
