import json
import os


FILE = "data/notifications.json"


class NotificationRepository:


    def __init__(self):

        os.makedirs(
            "data",
            exist_ok=True
        )


        if not os.path.exists(FILE):

            self.save_all([])



    def save_all(self, items):

        with open(FILE, "w") as f:

            json.dump(
                items,
                f,
                indent=2
            )



    def all(self):

        try:

            with open(FILE) as f:

                return json.load(f)

        except:

            return []



    def save(self, notification):

        items = self.all()

        items.append(
            notification.serialize()
        )

        self.save_all(
            items
        )

        return notification
