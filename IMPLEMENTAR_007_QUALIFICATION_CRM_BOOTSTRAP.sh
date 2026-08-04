#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 007 — Qualification Flow CRM Integration v0.1.0 ==="

mkdir -p companion/flows


cat > companion/flows/qualification.py <<'EOF'
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
EOF


cat > companion/flows/__init__.py <<'EOF'
"""
Conversation flows.
"""
EOF


echo ""
echo "=== VALIDACION QUALIFICATION CRM ==="


python3 - <<'EOF'

from companion.session import Session
from companion.context import Context
from companion.flows.qualification import handle


session = Session(
    channel="whatsapp"
)


context = Context(session)


context.update(
    "phone",
    "5210000000000"
)


context.update(
    "intent",
    "book_interest"
)


result = handle(context)


print(result)

EOF


echo ""
echo "=== IMPLEMENTAR 007 COMPLETADO ==="
