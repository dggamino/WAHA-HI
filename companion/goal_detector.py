"""
Goal Detection Foundation v0.1.0

Detecta objetivos operativos del Companion Engine.
"""


class GoalDetector:


    def detect(
        self,
        intent,
        context=None,
        message=None
    ):

        if intent == "book_interest":

            return {
                "goal": "book_information_request",
                "domain": "knowledge",
                "target": "HEREDITARIA_books"
            }


        if intent in [
            "consultation",
            "consultation_request"
        ]:

            return {
                "goal": "consultation_request",
                "domain": "service",
                "target": "consultation_flow"
            }


        if context:

            memory = context.get(
                "memory",
                {}
            )

            if memory:

                return {
                    "goal": "continue_previous_context",
                    "domain": "conversation",
                    "target": "memory_resume"
                }


        return {
            "goal": "intent_discovery",
            "domain": "conversation",
            "target": "unknown"
        }
