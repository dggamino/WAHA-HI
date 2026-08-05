"""
Goal-Oriented Action Planner Foundation v0.1.0

Transforma decisiones del Companion Engine
en planes operativos.
"""


class ActionPlanner:


    def plan(
        self,
        decision,
        intent=None,
        message=None
    ):

        if decision is None:

            return {
                "goal": "unknown",
                "intent": intent,
                "actions": []
            }


        action = decision.get(
            "action",
            ""
        )


        if action == "continue_flow":

            return {
                "goal": "continue_conversation_flow",
                "intent": intent,
                "actions": [
                    "restore_context",
                    "execute_flow",
                    "generate_response",
                    "update_memory"
                ]
            }


        if action == "resume_context":

            return {
                "goal": "resume_previous_context",
                "intent": intent,
                "actions": [
                    "load_memory",
                    "restore_intent",
                    "execute_flow",
                    "generate_response"
                ]
            }


        return {
            "goal": "discover_intent",
            "intent": intent,
            "actions": [
                "classify_message",
                "select_flow",
                "generate_response",
                "store_memory"
            ]
        }
