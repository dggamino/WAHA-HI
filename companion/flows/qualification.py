"""
Qualification Flow

Conecta intención conversacional
con registro CRM.
"""


from crm.service import CRMService
from crm.status import (
    BOOK_INTEREST,
    QUALIFIED,
    CONSULTATION_REQUESTED
)


crm = CRMService()


def qualify(phone, intent):

    prospect = crm.create_prospect(phone)


    if intent == "book_interest":

        crm.update_status(
            prospect.id,
            BOOK_INTEREST
        )


    elif intent == "consultation_request":

        crm.update_status(
            prospect.id,
            CONSULTATION_REQUESTED
        )


    else:

        crm.update_status(
            prospect.id,
            QUALIFIED
        )


    return prospect



def handle(context):

    phone = context.data.get(
        "phone",
        "unknown"
    )

    intent = context.data.get(
        "intent"
    )


    prospect = qualify(
        phone,
        intent
    )


    context.update(
        "prospect_id",
        prospect.id
    )


    return {

        "type": "action",

        "action": "crm_update",

        "prospect": {

            "id": prospect.id,

            "status": prospect.status

        }

    }
