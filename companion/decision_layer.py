"""
Companion Decision Layer Foundation v0.1.0

Capa de decisión basada en memoria y flujo.
"""


class DecisionLayer:


    def decide(
        self,
        message,
        memory=None,
        selected_flow=None
    ):

        if selected_flow:

            return {
                "action": "continue_flow",
                "flow": selected_flow.get("flow"),
                "intent": selected_flow.get("intent"),
                "reason": selected_flow.get("reason")
            }


        if memory:

            intent = memory.get(
                "last_intent",
                ""
            )

            if intent:

                return {
                    "action": "resume_context",
                    "intent": intent,
                    "reason": "memory_available"
                }


        return {
            "action": "classify",
            "intent": "",
            "reason": "no_context"
        }
