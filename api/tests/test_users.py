from unittest import TestCase
from flask import json
from api.views.app import app
from api.views.functions import users

sample_user = {
    'email': 'john@doe.com',
    'name': 'John Doe',
    'password': 'password',
    'rights': "Admin"
}

sample_user_missing= {
    'email': '',
    'name': '',
    'password': 'password',
    'rights': "Admin"
}

invalid_email_signup = {
    'email': 'johndoe.com',
    'name': 'John Doe',
    'password': 'password',
    'rights': "Admin"
}

sample_login = {
    'email': 'john@doe.com',
    'password': 'password'
}


class SalesTestCase(TestCase):

    def setUp(self):
        self.testclient = app.test_client()
        self.users = users

    def test_user_signup(self):
        response = self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                                        data=json.dumps(sample_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Success", response.data)

    def test_user_signup_missing_info(self):
        response = self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                                        data=json.dumps(sample_user_missing))
        self.assertEquals(response.status_code, 400)
        self.assertIn(b"Invalid request/input", response.data)

    def test_user_signup_missing_fields(self):
        response = self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                                        data=json.dumps(sample_login))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"A key error has been detected", response.data)

    def test_invalid_email(self):
        response = self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                                        data=json.dumps(invalid_email_signup))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email", response.data)

    def test_duplicate_user(self):
        self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                                        data=json.dumps(sample_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"already exists", response.data)

    def test_user_login(self):
        self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/login', content_type="application/json",
                                        data=json.dumps(sample_login))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User Logged in successfuly", response.data)

    def test_wrong_login(self):
        self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/login', content_type="application/json",
                                        data=json.dumps({'email': 'some@email.com', 'password': 'badpassword'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wrong login information", response.data)

    def test_no_login_values(self):
        self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/login', content_type="application/json",
                                        data=json.dumps({'email': '', 'password': ''}))
        self.assertEquals(response.status_code, 400)
        self.assertIn(b"Invalid request/input", response.data)

    def test_get_all_users(self):
        response = self.testclient.get('/store-manager/api/v1/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Users", response.data)

    def test_get_user_by_id(self):
        self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.get('/store-manager/api/v1/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user_id", response.data)
        self.assertEqual(users[0]['user_id'], 1)

    def test_get_user_not_found(self):
        self.testclient.post('/store-manager/api/v1/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.get('/store-manager/api/v1/users/10')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No user with ID '10' in the database", response.data)

    def tearDown(self):
        self.users.clear()
