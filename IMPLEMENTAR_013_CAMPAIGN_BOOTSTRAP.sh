#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 013 — Campaign & Funnel Layer Foundation v0.1.0 ==="

mkdir -p campaigns


touch campaigns/__init__.py


cat > campaigns/__init__.py <<'EOF'
"""
Campaign and Funnel Layer
"""
EOF


cat > campaigns/models.py <<'EOF'
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Campaign:

    id: str
    name: str
    source: str
    asset: str
    created_at: str = ""


    def __post_init__(self):

        if not self.created_at:

            self.created_at = datetime.now().isoformat()
EOF


cat > campaigns/registry.py <<'EOF'
"""
HEREDITARIA Campaign Registry
"""


CAMPAIGNS = {


    "HER-BOOK-001": {

        "name":
        "Libro Fundacional HEREDITARIA",

        "asset":
        "fundacional",

        "source":
        "whatsapp"

    },


    "HER-BOOK-002": {

        "name":
        "Libro del Cuidador",

        "asset":
        "cuidador",

        "source":
        "whatsapp"

    },


    "HER-BOOK-003": {

        "name":
        "Libro del Patrimonio Invisible",

        "asset":
        "patrimonio",

        "source":
        "whatsapp"

    }


}


def get_campaign(campaign_id):

    return CAMPAIGNS.get(
        campaign_id
    )


def list_campaigns():

    return CAMPAIGNS
EOF


cat > campaigns/service.py <<'EOF'
from .registry import get_campaign


class CampaignService:


    def resolve(self, campaign_id):

        campaign = get_campaign(
            campaign_id
        )


        if not campaign:

            return {

                "status":
                "NOT_FOUND"

            }


        return {

            "status":
            "FOUND",

            "campaign":
            campaign

        }
EOF


cat > campaigns/funnel.py <<'EOF'
"""
Funnel states.
"""


VISITOR = "VISITOR"

INTEREST = "INTEREST"

QUALIFIED = "QUALIFIED"

CONSULTATION = "CONSULTATION"

CLIENT = "CLIENT"
EOF


cat > campaigns/README.md <<'EOF'
# Campaign & Funnel Layer

Responsabilidades:

- Registrar campañas.
- Asociar origen.
- Medir atribución.

No contiene:

- conocimiento editorial.
- conversación.
- CRM.
EOF


echo ""
echo "=== VALIDACION CAMPAIGN LAYER ==="

python3 - <<'EOF'

from campaigns.service import CampaignService


service = CampaignService()


result = service.resolve(
    "HER-BOOK-001"
)


print(result)

EOF


echo ""
echo "=== IMPLEMENTAR 013 COMPLETADO ==="
