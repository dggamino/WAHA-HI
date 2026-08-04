import json
import os


SESSION_FILE = "data/sessions.json"


class SessionStore:


    def __init__(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        if not os.path.exists(SESSION_FILE):

            self._write({})



    def _write(self, data):

        with open(
            SESSION_FILE,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=2
            )



    def all(self):

        try:

            with open(
                SESSION_FILE,
                "r"
            ) as file:

                content = file.read()

                if not content.strip():

                    return {}


                return json.loads(content)


        except (
            json.JSONDecodeError,
            FileNotFoundError
        ):

            self._write({})

            return {}



    def save(self, session):

        sessions = self.all()


        sessions[
            session.session_id
        ] = session.serialize()


        self._write(
            sessions
        )



    def get(self, session_id):

        sessions = self.all()

        return sessions.get(
            session_id
        )
