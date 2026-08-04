"""
Multi-Turn Conversation Flow Foundation v0.1.0
"""


class ConversationResolver:


    def resolve(
        self,
        message,
        context
    ):

        if context is None:
            return message


        previous_intent = context.get(
            "intent",
            ""
        )


        if previous_intent == "book_interest":

            references = {
                "primero": "Libro Fundacional HEREDITARIA",
                "segundo": "Libro del Cuidador",
                "tercero": "Libro del Patrimonio Invisible"
            }


            lower = message.lower()

            for key, value in references.items():

                if key in lower:

                    return (
                        f"Quiero información sobre {value}"
                    )


        return message
