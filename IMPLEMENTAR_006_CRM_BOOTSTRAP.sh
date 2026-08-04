#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 006 — CRM Prospect Foundation v0.1.0 ==="

mkdir -p crm


touch crm/__init__.py


cat > crm/__init__.py <<'EOF'
"""
CRM Prospect Layer

Gestiona estados de prospectos.
"""
EOF


cat > crm/models.py <<'EOF'
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Prospect:

    id: str
    phone: str
    name: str = ""
    status: str = "NEW"
    created_at: str = ""


    def __post_init__(self):

        if not self.created_at:
            self.created_at = datetime.now().isoformat()
EOF


cat > crm/status.py <<'EOF'
"""
Estados comerciales iniciales.
"""


NEW = "NEW"

BOOK_INTEREST = "BOOK_INTEREST"

QUALIFIED = "QUALIFIED"

CONSULTATION_REQUESTED = "CONSULTATION_REQUESTED"

CLIENT = "CLIENT"

ESCALATED = "ESCALATED"
EOF


cat > crm/database.py <<'EOF'
"""
Persistencia inicial en memoria.

Futura migración:
SQLite/PostgreSQL.
"""


class CRMDatabase:


    def __init__(self):

        self.records = {}


    def save(self, prospect):

        self.records[prospect.id] = prospect

        return prospect


    def get(self, prospect_id):

        return self.records.get(prospect_id)


    def all(self):

        return list(self.records.values())
EOF


cat > crm/service.py <<'EOF'
import uuid

from .models import Prospect
from .database import CRMDatabase
from .status import NEW


class CRMService:


    def __init__(self):

        self.db = CRMDatabase()


    def create_prospect(self, phone):

        prospect = Prospect(

            id=str(uuid.uuid4()),

            phone=phone,

            status=NEW

        )

        return self.db.save(prospect)


    def update_status(self, prospect_id, status):

        prospect = self.db.get(prospect_id)

        if prospect:

            prospect.status = status

        return prospect
EOF


cat > crm/README.md <<'EOF'
# CRM Prospect Foundation

Capa inicial de gestión de prospectos.

Responsabilidades:

- Crear prospectos.
- Mantener estados.
- Registrar evolución comercial.

No contiene:
- lógica conversacional.
- contenido editorial.
- transporte WhatsApp.
EOF



echo ""
echo "=== VALIDACION CRM ==="

python3 - <<'EOF'

from crm.service import CRMService
from crm.status import BOOK_INTEREST


crm = CRMService()


lead = crm.create_prospect(
    "5210000000000"
)


crm.update_status(
    lead.id,
    BOOK_INTEREST
)


print(lead)

EOF


echo ""
echo "=== IMPLEMENTAR 006 COMPLETADO ==="
