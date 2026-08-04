"""
Text Response Builder Foundation v0.1.0
"""

class TextResponder:

    def build(self, result):

        if result.get("flow") == "books":

            books = result.get("books", [])

            lines = [
                "Libros HEREDITARIA disponibles:"
            ]

            for index, book in enumerate(books, 1):
                lines.append(
                    f"{index}. {book['title']}"
                )

            return "\n".join(lines)

        return "No encontré información disponible."
