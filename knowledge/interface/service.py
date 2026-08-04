"""
Knowledge retrieval service.
"""


from knowledge.interface.repository import KnowledgeRepository



class KnowledgeService:


    def __init__(self):

        self.repository = KnowledgeRepository()



    def search(self, query):

        results = self.repository.find(
            query
        )


        return {

            "query":
            query,

            "results":
            results

        }



    def catalog(self):

        return self.repository.list()
