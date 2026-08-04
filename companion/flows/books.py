from companion.adapters.knowledge import get_books


class BooksFlow:

    def execute(self, context):

        if hasattr(context, "update"):

            try:
                context.update(
                    "flow",
                    "books"
                )

            except TypeError:
                context.update(
                    {
                        "flow": "books"
                    }
                )

        books = get_books()

        if isinstance(books, dict):
            books = books.values()

        titles = [
            book["title"]
            for book in books
        ]

        return {
            "type": "text",
            "content":
                "Libros HEREDITARIA disponibles: "
                + ", ".join(titles)
        }


def handle(context):

    return BooksFlow().execute(context)
