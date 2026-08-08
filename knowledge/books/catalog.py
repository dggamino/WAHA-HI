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

    },


    "cuentaselo_padres": {

        "id":
        "HER-BOOK-CTP",

        "title":
        "Cuéntaselo a tus Padres",

        "category":
        "puente familiar",

        "content":
        "Libro-regalo breve para acompañar la primera conversación sobre "
        "el valor de la casa familiar, sin presión ni tecnicismos. "
        "Capítulos completos disponibles próximamente.",

        "chapters_path":
        "knowledge/books/metadata/cuentaselo-a-tus-padres/",

        "fundamento_legal":
        "Decreto Número 87, Gaceta del Gobierno del Estado de México, 7 de mayo de 2013"

    }


}


def get_books():

    return BOOKS

def catalog():
    return get_books()
