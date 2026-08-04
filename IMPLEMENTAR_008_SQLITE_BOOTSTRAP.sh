#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 008 — Persistence Layer SQLite v0.1.0 ==="

mkdir -p data


cat > crm/sqlite.py <<'EOF'
"""
SQLite Persistence Layer

Almacenamiento local CRM.
"""

import sqlite3
from pathlib import Path


DB_PATH = Path("data/prospects.db")


class SQLiteCRM:


    def __init__(self):

        self.connection = sqlite3.connect(
            DB_PATH
        )

        self.create_tables()


    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS prospects (

                id TEXT PRIMARY KEY,

                phone TEXT NOT NULL,

                name TEXT,

                status TEXT,

                created_at TEXT

            )
            """
        )

        self.connection.commit()



    def save(self, prospect):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO prospects
            VALUES (?, ?, ?, ?, ?)
            """,

            (
                prospect.id,
                prospect.phone,
                prospect.name,
                prospect.status,
                prospect.created_at
            )
        )

        self.connection.commit()

        return prospect



    def update_status(
        self,
        prospect_id,
        status
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE prospects
            SET status=?
            WHERE id=?
            """,

            (
                status,
                prospect_id
            )
        )

        self.connection.commit()



    def get(self, prospect_id):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM prospects
            WHERE id=?
            """,

            (
                prospect_id,
            )
        )

        return cursor.fetchone()



    def all(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM prospects
            """
        )

        return cursor.fetchall()
EOF


cat > crm/service.py <<'EOF'
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
EOF


echo ""
echo "=== VALIDACION SQLITE CRM ==="


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


print(
    "CREATED:",
    lead.id
)


print(
    "DATABASE:",
    crm.list_prospects()
)

EOF


echo ""
echo "=== IMPLEMENTAR 008 COMPLETADO ==="
