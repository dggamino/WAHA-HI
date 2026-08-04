import uuid

from .models import Prospect
from .sqlite import SQLiteCRM
from .status import NEW


class CRMService:


    def __init__(self):

        self.db = SQLiteCRM()



    def create_prospect(
        self,
        phone
    ):

        prospect = Prospect(

            id=str(uuid.uuid4()),

            phone=phone,

            status=NEW

        )


        return self.db.save(
            prospect
        )



    def update_status(
        self,
        prospect_id,
        status
    ):

        self.db.update_status(
            prospect_id,
            status
        )

        return self.db.get(
            prospect_id
        )



    def list_prospects(self):

        return self.db.all()
