import uuid

from sessions.models import SessionRecord
from sessions.store import SessionStore



class SessionService:


    def __init__(self):

        self.store = SessionStore()



    def create(
        self,
        user_id,
        channel="whatsapp"
    ):

        session = SessionRecord(

            session_id=str(
                uuid.uuid4()
            ),

            channel=channel,

            user_id=user_id,

            state={}

        )


        self.store.save(
            session
        )


        return session



    def update_state(
        self,
        session_id,
        key,
        value
    ):

        data = self.store.get(
            session_id
        )


        if not data:

            return None


        data["state"][key] = value


        with open(
            "data/sessions.json",
            "w"
        ) as file:

            import json

            sessions = self.store.all()

            sessions[session_id] = data

            json.dump(
                sessions,
                file,
                indent=2
            )


        return data
