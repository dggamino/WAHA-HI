"""
HEREDITARIA Editorial Catalog
"""


BOOKS = {


    "fundacional": {

        "id":
        "HER-BOOK-001",

        "title":
        "Libro Fundacional HEREDITARIA",

        "category":
        "foundation",

        "content":
        "Marco conceptual del sistema HEREDITARIA."

    },


    "cuidador": {

        "id":
        "HER-BOOK-002",

        "title":
        "Libro del Cuidador",

        "category":
        "care",

        "content":
        "Documentación de la experiencia del cuidador."

    },


    "patrimonio": {

        "id":
        "HER-BOOK-003",

        "title":
        "Libro del Patrimonio Invisible",

        "category":
        "heritage",

        "content":
        "Registro del valor patrimonial no visible."

    }


}


def get_books():

    return BOOKS

def catalog():
    return get_books()
