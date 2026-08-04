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
