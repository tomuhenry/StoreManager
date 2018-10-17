import unittest
from api.app import app

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.testclient = app.test_client()

if __name__ =="__main__":
    unittest.main()