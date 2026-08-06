from dataclasses import dataclass, field

@dataclass
class ConversationContext:
    session_id: str
    user_id: str
    intent: str = ""
    state: str = "NEW"
    memory: dict = field(default_factory=dict)
    knowledge: list = field(default_factory=list)

    def __post_init__(self):
        if self.memory is None:
            self.memory = {}
        if self.knowledge is None:
            self.knowledge = []

    def update(self, key, value):
        """Actualiza un campo dinámicamente (compatibilidad con Context API)"""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            # Si no es un campo conocido, guardar en memory
            self.memory[key] = value

    def update_state(self, state):
        self.state = state

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "intent": self.intent,
            "state": self.state,
            "memory": self.memory,
            "knowledge": self.knowledge
        }
