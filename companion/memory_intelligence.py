"""
Conversation Memory Intelligence Foundation v0.1.0
"""


from datetime import datetime


class MemoryIntelligence:


    def enrich(
        self,
        message,
        intent,
        result=None
    ):

        memory = {
            "last_message": message,
            "last_intent": intent,
            "updated_at": datetime.now().isoformat()
        }


        if intent == "book_interest":

            memory["conversation"] = {
                "topic": "HEREDITARIA",
                "stage": "exploration"
            }


            if result and "books" in result:

                memory["conversation"]["available_options"] = [
                    book["title"]
                    for book in result["books"]
                ]


        return memory
