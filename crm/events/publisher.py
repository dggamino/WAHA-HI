"""
Publishes CRM events into Ledger.
"""


import uuid
from datetime import datetime


class CRMEventPublisher:


    def __init__(self, ledger):

        self.ledger = ledger



    def prospect_created(self, prospect):

        event = {

            "prospect_id":
            prospect.prospect_id,

            "user_id":
            prospect.user_id,

            "intent":
            prospect.intent,

            "interest_level":
            prospect.interest_level

        }


        return self.ledger.record(

            event_type="CRM_PROSPECT_CREATED",

            source="crm",

            payload=event

        )
