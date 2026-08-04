"""
Conversation Context Service.
"""


from companion.context.merge import ContextMerger



class ContextService:


    def __init__(self):

        self.merger = ContextMerger()



    def create_context(
        self,
        session,
        intent,
        query
    ):

        return self.merger.build(

            session,

            intent,

            query

        )
