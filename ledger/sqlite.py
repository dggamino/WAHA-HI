import sqlite3
from pathlib import Path


DB_PATH = Path("data/events.db")


class EventLedger:


    def __init__(self):

        self.connection = sqlite3.connect(
            DB_PATH
        )

        self.create_table()



    def create_table(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (

                id TEXT PRIMARY KEY,

                event_type TEXT,

                source TEXT,

                payload TEXT,

                created_at TEXT

            )
            """
        )

        self.connection.commit()



    def append(self, event):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO events
            VALUES (?, ?, ?, ?, ?)
            """,

            (
                event.id,
                event.event_type,
                event.source,
                event.payload,
                event.created_at
            )

        )

        self.connection.commit()

        return event



    def list_events(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM events
            ORDER BY created_at
            """
        )

        return cursor.fetchall()
