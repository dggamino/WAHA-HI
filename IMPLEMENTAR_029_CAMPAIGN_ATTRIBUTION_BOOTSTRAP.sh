#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 029 — Campaign Attribution Engine Foundation v0.1.0 ==="


mkdir -p attribution


touch attribution/__init__.py


cat > attribution/__init__.py <<'EOF'
"""
Campaign Attribution Layer
"""
EOF


cat > attribution/models.py <<'EOF'
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class AttributionRecord:

    prospect_id: str
    campaign: str
    channel: str
    source: str
    created_at: str = ""


    def __post_init__(self):

        if not self.created_at:

            self.created_at = datetime.now().isoformat()


    def serialize(self):

        return asdict(self)
EOF


cat > attribution/engine.py <<'EOF'
"""
Campaign attribution engine.
"""


from attribution.models import AttributionRecord



class AttributionEngine:


    def attribute(

        self,

        prospect_id,

        campaign="organic",

        channel="whatsapp",

        source="conversation"

    ):


        return AttributionRecord(

            prospect_id=prospect_id,

            campaign=campaign,

            channel=channel,

            source=source

        )
EOF


cat > attribution/repository.py <<'EOF'
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
EOF


cat > attribution/service.py <<'EOF'
from attribution.repository import AttributionRepository



class AttributionService:


    def __init__(self):

        self.repository = AttributionRepository()



    def register(self, record):

        return self.repository.save(
            record
        )
EOF


cat > attribution/README.md <<'EOF'
# Campaign Attribution Engine

Relaciona prospectos con:

- campaña
- canal
- fuente

No administra:

- CRM
- conversación
- conocimiento
EOF


echo ""
echo "=== VALIDACION ATTRIBUTION ==="

python3 - <<'EOF'

from qualification.engine import QualificationEngine
from crm.integration.service import CRMLeadService
from attribution.engine import AttributionEngine
from attribution.service import AttributionService


qualification = QualificationEngine()


lead = qualification.qualify(

    "5210000000000",

    "book_interest"

)


crm = CRMLeadService()


prospect = crm.create_from_lead(
    lead
)


engine = AttributionEngine()


record = engine.attribute(

    prospect.prospect_id,

    "libro_fundacional",

    "whatsapp",

    "organic"

)


service = AttributionService()


saved = service.register(
    record
)


print(
    saved.serialize()
)

EOF


echo ""
echo "=== IMPLEMENTAR 029 COMPLETADO ==="
