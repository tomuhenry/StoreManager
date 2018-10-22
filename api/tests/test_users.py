from unittest import TestCase
from flask import json
from api.endpoints.app import app
from api.endpoints.functions import users

sample_user = {
        'email': 'john@doe.com',
        'name': 'John Doe',
        'password': 'password',
        'rights': "Admin"
    }


class SalesTestCase(TestCase):

    def setUp(self):
        self.testclient = app.test_client()
        self.users = users

    def test_user_signup(self):
        response = self.testclient.post('/store-manager/api/v1', content_type="application/json",
                                        data=json.dumps(sample_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Success", response.data)

    def test_email_validity(self):
        pass

    def test_duplicate_user(self):
        self.testclient.post('/store-manager/api/v1', content_type="application/json",
                                        data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1', content_type="application/json",
                                        data=json.dumps(sample_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"already exists", response.data)

    def tearDown(self):
        self.users.clear()