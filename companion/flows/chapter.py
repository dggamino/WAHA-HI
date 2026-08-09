import re
import unicodedata
from knowledge.books.catalog import catalog
from knowledge.books.loader import get_chapter


def _strip_accents(text):
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def _clean_words(text):
    """Extrae palabras limpias (sin puntuación, sin acentos, minúsculas)."""
    text = _strip_accents(text.lower())
    text = re.sub(r'[^\w\s]', ' ', text)
    return set(w for w in text.split() if len(w) >= 3)


_STOPWORDS = {
    "que", "por", "del", "los", "las", "una", "con", "para", "como", "mas",
    "sin", "son", "tan", "pero", "este", "esta", "esto", "ese", "esa", "eso",
    "el", "la", "lo", "le", "me", "te", "se", "ya", "al", "un", "en", "de",
    "los", "las", "con", "para", "como", "mas", "sin", "sobre", "entre",
    "hasta", "desde", "ante", "bajo", "tras", "durante", "mediante", "segun",
    "cabe", "excepto", "salvo", "incluso", "mas", "menos", "aun", "aunque",
    "mientras", "cuando", "donde", "quien", "cuyo", "cuya", "cuyos", "cuyas",
    "tal", "tales", "cual", "cuales", "cuanto", "cuanta", "cuantos", "cuantas",
    "mismo", "misma", "mismos", "mismas", "tan", "tanto", "tanta", "tantos",
    "tantas", "bien", "mal", "asi", "aqui", "alla", "aca", "alli", "ahora",
    "antes", "despues", "luego", "pronto", "tarde", "temprano", "todavia",
    "ya", "aun", "tambien", "tampoco", "solo", "solamente", "apenas", "casi",
    "quizas", "quiza", "acaso", "talvez", "probablemente", "posiblemente",
    "seguramente", "ciertamente", "realmente", "verdaderamente", "efectivamente",
    "efecto", "hecho", "verdad", "falso", "cierto", "seguro", "probable",
    "posible", "imposible", "necesario", "necesaria", "necesarios", "necesarias",
    "importante", "importantes", "principal", "principales", "fundamental",
    "fundamentales", "basico", "basicos", "esencial", "esenciales", "minimo",
    "minimos", "maximo", "maximos", "mejor", "mejores", "peor", "peores",
    "mayor", "mayores", "menor", "menores", "primero", "primera", "primeros",
    "primeras", "ultimo", "ultima", "ultimos", "ultimas", "siguiente",
    "siguientes", "anterior", "anteriores", "mismo", "misma", "mismos", "mismas",
    "otro", "otra", "otros", "otras", "tal", "tales", "cual", "cuales",
    "quien", "quienes", "cuyo", "cuya", "cuyos", "cuyas", "cuanto", "cuanta",
    "cuantos", "cuantas", "demasiado", "demasiada", "demasiados", "demasiadas",
    "bastante", "bastantes", "poco", "poca", "pocos", "pocas", "mucho", "mucha",
    "muchos", "muchas", "todo", "toda", "todos", "todas", "nada", "nadie",
    "ninguno", "ninguna", "ningunos", "ningunas", "alguien", "algo", "alguno",
    "alguna", "algunos", "algunas", "cualquiera", "cualesquiera", "varios",
    "varias", "demas", "resto", "restos", "demas", "mismo", "misma", "mismos",
    "mismas", "propio", "propia", "propios", "propias", "ajeno", "ajena",
    "ajenos", "ajenas", "particular", "particulares", "especial", "especiales",
    "general", "generales", "comun", "comunes", "normal", "normales", "usual",
    "usuales", "corriente", "corrientes", "ordinario", "ordinarios", "regular",
    "regulares", "tipico", "tipicos", "caracteristico", "caracteristicos",
    "constante", "constantes", "permanente", "permanentes", "continuo",
    "continua", "continuos", "continuas", "frecuente", "frecuentes", "habitual",
    "habituales", "costumbre", "costumbres", "acostumbrado", "acostumbrada",
    "acostumbrados", "acostumbradas", "suelo", "suele", "suelen", "solia",
    "solian", "acostumbro", "acostumbran", "solia", "solian"
}


def _word_overlap(text, title):
    """Devuelve True si al menos 2 palabras significativas del título están en el texto."""
    text_words = _clean_words(text)
    title_words = _clean_words(title)

    # Filtrar stopwords
    significant = title_words - _STOPWORDS
    if not significant:
        significant = title_words

    matches = text_words & significant
    return len(matches) >= 2 or (len(significant) == 1 and len(matches) == 1)


class ChapterFlow:

    def execute(self, context):
        raw_text = context.memory.get("raw_text", "") or ""
        text_normalized = _strip_accents(raw_text.lower())

        match = re.search(r'capitulo\s*(\d+)', text_normalized)
        if not match:
            return {"type": "text", "content": "¿De qué capítulo hablas? Escribe, por ejemplo: capítulo 3"}

        chapter_num = int(match.group(1))

        books = catalog()
        matched_book = None
        text_lower = raw_text.lower()

        # Primero: match exacto por ID
        for book in books.values():
            if book["id"].lower() in text_lower:
                matched_book = book
                break

        # Segundo: match por palabras del título
        if not matched_book:
            for book in books.values():
                if _word_overlap(raw_text, book["title"]):
                    matched_book = book
                    break

        if not matched_book:
            return {
                "type": "text",
                "content": "Dime también el nombre del libro, ej: 'capítulo 3 de La casa no se toca'"
            }

        chapter = get_chapter(matched_book.get("chapters_path", ""), chapter_num)
        if not chapter:
            return {"type": "text", "content": f"No encontré el capítulo {chapter_num} de {matched_book['title']}."}

        return {
            "type": "text",
            "content": f"*{chapter['seccion']}*\n\n{chapter['body']}"
        }


def handle(context):
    return ChapterFlow().execute(context)
