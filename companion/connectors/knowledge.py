"""
Knowledge connector for Companion.

Companion does not access knowledge storage directly.
"""


from knowledge.interface.service import KnowledgeService



class KnowledgeConnector:


    def __init__(self):

        self.service = KnowledgeService()



    def query(self, text):

        return self.service.search(
            text
        )



    def books(self):

        return self.service.catalog()
