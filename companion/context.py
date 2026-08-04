class Context:

    def __init__(self, session):
        self.session = session
        self.data = {
            "session_id": session.id,
            "intent": None,
            "flow": None,
            "metadata": {}
        }

    def update(self, key, value):
        self.data[key] = value
