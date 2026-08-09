import unicodedata
from companion.adapters.knowledge import get_books


def _strip_accents(text):
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


class BooksFlow:

    def execute(self, context):

        if hasattr(context, "update"):
            try:
                context.update("flow", "books")
            except TypeError:
                context.update({"flow": "books"})

        raw_text = ""
        if hasattr(context, "memory") and isinstance(context.memory, dict):
            raw_text = context.memory.get("raw_text", "") or ""

        text_normalized = _strip_accents(raw_text.lower())

        books = get_books()
        if isinstance(books, dict):
            books = list(books.values())

        # ─── Ruteo por keyword específica del libro ──────────────
        matched_book = None
        for book in books:
            book_keywords = book.get("keywords", [])
            for kw in book_keywords:
                kw_normalized = _strip_accents(kw.lower())
                if kw_normalized in text_normalized and kw_normalized not in ("libro", "libros"):
                    matched_book = book
                    break
            if matched_book:
                break

        if matched_book and matched_book.get("status") == "disponible" and matched_book.get("chapters_path"):
            return {
                "type": "text",
                "content": (
                    f"📖 *{matched_book['title']}*\n\n"
                    f"{matched_book['content']}\n\n"
                    f"Escribe *libros* para ver el catálogo completo."
                )
            }
        # ───────────────────────────────────────────────────────────

        disponibles = [b["title"] for b in books if b.get("status") == "disponible"]
        proximamente = [b["title"] for b in books if b.get("status") == "proximamente"]

        catalog_text = "📚 *Disponibles ahora:*\n" + "\n".join(f"• {t}" for t in disponibles)
        if proximamente:
            catalog_text += "\n\n🔜 *Próximamente:*\n" + "\n".join(f"• {t}" for t in proximamente)

        return {
            "type": "video",
            "media": "./assets/hereditaria-libro.mp4",
            "content": (
                "HEREDITARIA™ Vol. I\nLA CASA NO SE TOCA\n¿Ya viste por qué?\n\n"
                + catalog_text
            )
        }


def handle(context):
    return BooksFlow().execute(context)
