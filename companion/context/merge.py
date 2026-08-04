"""
Context aggregation layer.
"""


from companion.connectors.knowledge import KnowledgeConnector



class ContextMerger:


    def __init__(self):

        self.knowledge = KnowledgeConnector()



    def build(
        self,
        session,
        intent,
        query
    ):


        knowledge_result = self.knowledge.query(
            query
        )


        return {

            "session":

            {

                "id":
                session.session_id,

                "user":
                session.user_id

            },


            "intent":
            intent,


            "memory":
            session.state,


            "knowledge":
            knowledge_result["results"]

        }
