#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 027 — CRM Lead Persistence Integration Foundation v0.1.0 ==="

mkdir -p crm/integration


touch crm/integration/__init__.py


cat > crm/integration/__init__.py <<'EOF'
"""
CRM Integration Layer
"""
EOF


cat > crm/integration/models.py <<'EOF'
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ProspectRecord:

    prospect_id: str
    user_id: str
    intent: str
    interest_level: str
    source: str
    created_at: str = ""


    def __post_init__(self):

        if not self.created_at:

            self.created_at = datetime.now().isoformat()


    def serialize(self):

        return asdict(self)
EOF


cat > crm/integration/repository.py <<'EOF'
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
EOF


cat > crm/integration/service.py <<'EOF'
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
EOF


cat > crm/integration/README.md <<'EOF'
# CRM Lead Persistence Integration

Convierte:

LeadProfile

en:

ProspectRecord


Responsabilidad:

Persistencia comercial.

No administra:

- conversación.
- conocimiento.
- clasificación.
EOF


echo ""
echo "=== VALIDACION CRM INTEGRATION ==="

python3 - <<'EOF'

from qualification.engine import QualificationEngine
from crm.integration.service import CRMLeadService


qualification = QualificationEngine()

lead = qualification.qualify(

    "5210000000000",

    "book_interest"

)


crm = CRMLeadService()


prospect = crm.create_from_lead(
    lead
)


print(
    prospect.serialize()
)

EOF


echo ""
echo "=== IMPLEMENTAR 027 COMPLETADO ==="
