import json
import os


FILE = "data/followups.json"


class TaskRepository:


    def __init__(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        if not os.path.exists(FILE):

            self.save_all([])



    def save_all(self, tasks):

        with open(FILE, "w") as f:

            json.dump(
                tasks,
                f,
                indent=2
            )



    def all(self):

        try:

            with open(FILE) as f:

                return json.load(f)

        except:

            return []



    def save(self, task):

        tasks = self.all()

        tasks.append(
            task.serialize()
        )

        self.save_all(tasks)

        return task
