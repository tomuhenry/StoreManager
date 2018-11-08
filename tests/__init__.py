from unittest import TestCase
from api.database.database import Database

database_cls = Database()


class BaseTestCase(TestCase):

    def setUp(self):
        database_cls.create_tables()

    def tearDown(self):
        database_cls.drop_table("DROP TABLE sales")
        database_cls.drop_table("DROP TABLE products")
        database_cls.drop_table("DROP TABLE category")
        database_cls.drop_table("DROP TABLE users")
        database_cls.create_tables()
