import json
import os


CRM_FILE = "data/prospects.json"


class ProspectRepository:


    def __init__(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        if not os.path.exists(CRM_FILE):

            self.save_all({})



    def save_all(self, data):

        with open(
            CRM_FILE,
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
                CRM_FILE
            ) as file:

                return json.load(file)

        except:

            return {}



    def save(self, prospect):

        records = self.all()

        records[
            prospect.prospect_id
        ] = prospect.serialize()


        self.save_all(
            records
        )


        return prospect
