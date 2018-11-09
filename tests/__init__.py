from unittest import TestCase
from database.database import Database

database_cls = Database()


class BaseTestCase(TestCase):

    def setUp(self):
        database_cls.create_tables()

    def tearDown(self):
        database_cls.drop_table("sales")
        database_cls.drop_table("products")
        database_cls.drop_table("category")
        database_cls.drop_table("users")
        database_cls.create_tables()
