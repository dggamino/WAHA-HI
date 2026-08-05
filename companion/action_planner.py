"""
Adaptive Action Planning Foundation v0.1.0
"""


class ActionPlanner:


    def plan(
        self,
        intent,
        goal,
        decision=None,
        message=None
    ):

        goal_name = goal.get(
            "goal",
            "unknown"
        )


        if goal_name == "book_information_request":

            return {
                "goal": goal_name,
                "intent": intent,
                "domain": goal.get(
                    "domain"
                ),
                "target": goal.get(
                    "target"
                ),
                "actions": [
                    "load_catalog",
                    "identify_book_interest",
                    "generate_response",
                    "persist_interest"
                ]
            }


        if goal_name == "consultation_request":

            return {
                "goal": goal_name,
                "intent": intent,
                "domain": goal.get(
                    "domain"
                ),
                "target": goal.get(
                    "target"
                ),
                "actions": [
                    "load_service_context",
                    "qualify_request",
                    "generate_response",
                    "persist_lead"
                ]
            }


        if decision and decision.get(
            "action"
        ) == "continue_flow":

            return {
                "goal": "continue_previous_context",
                "intent": intent,
                "actions": [
                    "restore_context",
                    "execute_flow",
                    "generate_response",
                    "update_memory"
                ]
            }


        return {
            "goal": goal_name,
            "intent": intent,
            "actions": [
                "classify_message",
                "select_flow",
                "generate_response",
                "store_memory"
            ]
        }
