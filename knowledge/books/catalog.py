"""
HEREDITARIA Editorial Catalog
"""


BOOKS = {
    "fundacional": {
        "id": "HER-BOOK-001",
        "title": "Libro Fundacional HEREDITARIA",
        "category": "foundation",
        "content": "Marco conceptual del sistema HEREDITARIA."
    },
    "cuidador": {
        "id": "HER-BOOK-002",
        "title": "Libro del Cuidador",
        "category": "care",
        "content": "Documentación de la experiencia del cuidador."
    },
    "patrimonio": {
        "id": "HER-BOOK-003",
        "title": "Libro del Patrimonio Invisible",
        "category": "heritage",
        "content": "Registro del valor patrimonial no visible."
    },
    "cuentaselo_padres": {
        "id": "HER-BOOK-CTP",
        "title": "Cuéntaselo a tus Padres",
        "category": "puente familiar",
        "content": "Libro-regalo breve para acompañar la primera conversación sobre "
                   "el valor de la casa familiar, sin presión ni tecnicismos. "
                   "Capítulos completos disponibles próximamente.",
        "chapters_path": "knowledge/books/metadata/cuentaselo-a-tus-padres/",
        "fundamento_legal": "Decreto Número 87, Gaceta del Gobierno del Estado de México, 7 de mayo de 2013"
    },
    "casa_no_se_toca": {
        "id": "HER-BOOK-CST",
        "title": "La casa no se toca. ¿Por quién?",
        "category": "Derecho patrimonial familiar",
        "content": "Libro de Daniel Gómez Gamiño sobre la Hipoteca Inversa en el Estado de México: "
                   "por qué la frase 'la casa no se toca' protege al heredero anticipado en lugar del propietario, "
                   "qué es la cleptonomía familiar, y cómo el Decreto 87 permite convertir el valor de una casa "
                   "en ingresos mensuales sin venderla. 7 capítulos + epílogo + nota legal.",
        "chapters_path": "knowledge/books/metadata/casa-no-se-toca/",
        "author": "Daniel Gómez Gamiño",
        "year": 2026,
        "keywords": ["CASA", "PENSIÓN", "ESCRITURA", "TESTAMENTO", "NOTARIO", "PADRES"],
        "fundamento_legal": "Decreto Número 87, Gaceta del Gobierno del Estado de México, 7 de mayo de 2013",
        "audience": "Punto de entrada — cualquier lector",
        "tier": "Biblioteca"
    },
    "cuadrante_patrimonio": {
        "id": "HER-BOOK-CPF",
        "title": "El Cuadrante del Patrimonio Familiar",
        "category": "Diagnóstico familiar",
        "content": "Marco de cuatro cuadrantes para diagnosticar la posición de cada miembro de la familia "
                   "frente al patrimonio: Congelado, Calculador, Validador y Planeador. "
                   "Incluye cómo moverse entre cuadrantes y por qué el cuadrante se transmite como herencia. "
                   "7 capítulos + epílogo + nota legal.",
        "chapters_path": "knowledge/books/metadata/cuadrante-patrimonio-familiar/",
        "author": "Daniel Gómez Gamiño",
        "year": 2026,
        "keywords": ["PADRES", "CASA", "PENSIÓN", "TESTAMENTO", "CUIDADOR", "NOTARIO"],
        "fundamento_legal": "Decreto Número 87, Gaceta del Gobierno del Estado de México, 7 de mayo de 2013",
        "audience": "El marco de diagnóstico completo",
        "tier": "Biblioteca"
    }
}


def get_books():
    return BOOKS


def catalog():
    return get_books()




