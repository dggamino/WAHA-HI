"""
Memory Driven Flow Selection Foundation v0.1.0
"""


class MemoryFlowSelector:


    def select(
        self,
        message,
        memory=None
    ):

        if not memory:
            return None


        last_intent = memory.get(
            "last_intent",
            ""
        )


        topic = memory.get(
            "topic",
            ""
        )


        text = message.lower().strip()


        if (
            last_intent == "book_interest"
            and topic == "HEREDITARIA"
        ):

            if text in [
                "hola",
                "buenas",
                "buenos dias",
                "buenas tardes"
            ]:

                return {
                    "flow": "books",
                    "intent": "book_interest",
                    "reason": "memory_continuation"
                }


        return None
