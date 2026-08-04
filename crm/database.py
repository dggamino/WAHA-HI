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
