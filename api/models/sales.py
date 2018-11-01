from api.database.database import Database
from datetime import datetime

class Sales:
    def __init__(self):
        self.database_cls = Database()
        self.time = datetime.now()

    def make_a_sale(self):
        pass