class Memory:

    def __init__(self):
        self.storage = {}

    def save(self, session_id, data):
        self.storage[session_id] = data

    def load(self, session_id):
        return self.storage.get(session_id, {})
