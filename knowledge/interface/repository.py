"""
Knowledge repository.
"""


from knowledge.books.catalog import get_books


class KnowledgeRepository:


    def list(self):

        return get_books()



    def find(self, keyword):

        books = get_books()


        results = []


        for book in books.values():

            text = (

                book["title"]
                +
                " "
                +
                book["content"]

            ).lower()


            if keyword.lower() in text:

                results.append(book)


        return results
