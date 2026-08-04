import json
import os


FILE = "data/attributions.json"



class AttributionRepository:


    def __init__(self):

        os.makedirs(
            "data",
            exist_ok=True
        )


        if not os.path.exists(FILE):

            self.save_all({})



    def save_all(self,data):

        with open(
            FILE,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )



    def save(self, record):

        data = self.load()

        data[
            record.prospect_id
        ] = record.serialize()


        self.save_all(data)

        return record



    def load(self):

        try:

            with open(FILE) as f:

                return json.load(f)

        except:

            return {}
