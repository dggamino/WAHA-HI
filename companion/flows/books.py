from companion.adapters.knowledge import get_books


class BooksFlow:

    def execute(self, context):

        if hasattr(context, "update"):
            try:
                context.update("flow", "books")
            except TypeError:
                context.update({"flow": "books"})

        books = get_books()

        if isinstance(books, dict):
            books = books.values()

        titles = [book["title"] for book in books]

        return {
            "type": "video",
            "media": "./assets/hereditaria-libro.mp4",
            "content": (
                "HEREDITARIA™ Vol. I\nLA CASA NO SE TOCA\n¿Ya viste por qué?\n\n"
                "Libros disponibles: " + ", ".join(titles)
            )
        }


def handle(context):
    return BooksFlow().execute(context)
