from dataclasses import dataclass


@dataclass
class ConversationContext:

    session_id: str
    user_id: str
    intent: str = ""
    memory: dict = None
    knowledge: list = None


    def __post_init__(self):

        if self.memory is None:

            self.memory = {}


        if self.knowledge is None:

            self.knowledge = []
