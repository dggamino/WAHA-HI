"""
Conversation State Machine Foundation v0.1.0
"""


class ConversationStateMachine:

    STATES = [
        "NEW",
        "GREETING",
        "INTENT_DETECTED",
        "FLOW_ACTIVE",
        "WAITING_INPUT",
        "COMPLETED"
    ]


    def __init__(self, initial="NEW"):

        if initial not in self.STATES:
            initial = "NEW"

        self.state = initial


    def transition(self, new_state):

        if new_state not in self.STATES:
            raise ValueError(
                f"Invalid state: {new_state}"
            )

        self.state = new_state

        return self.state


    def current_state(self):

        return self.state


    def to_dict(self):

        return {
            "state": self.state
        }
