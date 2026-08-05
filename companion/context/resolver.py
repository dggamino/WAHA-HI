"""
Conversation Resolver

Semantic Reference Resolution Foundation v0.4.0
"""


class ConversationResolver:


    def resolve(
        self,
        message,
        context=None
    ):

        if not context:
            return message


        memory = context.get(
            "memory",
            {}
        )


        intent = (
            context.get("intent")
            or memory.get("last_intent")
        )


        # Compatibilidad:
        # memoria plana y memoria encapsulada

        options = memory.get(
            "available_options",
            []
        )


        if not options:

            conversation = memory.get(
                "conversation",
                {}
            )

            options = conversation.get(
                "available_options",
                []
            )


        text = message.lower().strip()


        if intent == "book_interest" and options:


            mapping = {
                "primero": 0,
                "primer": 0,
                "segundo": 1,
                "segundo libro": 1,
                "tercero": 2,
                "tercer": 2,
                "1": 0,
                "2": 1,
                "3": 2,
            }


            for key, index in mapping.items():

                if key in text:

                    if index < len(options):

                        return (
                            "Quiero información sobre "
                            + options[index]
                        )


        return message
