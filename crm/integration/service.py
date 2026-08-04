import uuid

from crm.integration.models import ProspectRecord
from crm.integration.repository import ProspectRepository



class CRMLeadService:


    def __init__(self):

        self.repository = ProspectRepository()



    def create_from_lead(
        self,
        lead
    ):


        prospect = ProspectRecord(

            prospect_id=str(
                uuid.uuid4()
            ),

            user_id=lead.user_id,

            intent=lead.intent,

            interest_level=lead.interest_level,

            source=lead.source

        )


        return self.repository.save(
            prospect
        )
