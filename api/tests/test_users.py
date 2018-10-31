from unittest import TestCase
from flask import json
from api.views import app
from api.database.database import Database

sample_user = {
    "name": "tom1 Admin",
    "email": "admin@trueadmin.com",
    "password": "adminpassword",
    "rights": 'false'
}

class SalesTestCase(TestCase):

    def setUp(self):
        database_cls = Database()
        self.testclient = app.test_client()

    def test_user_signup(self):
        response = self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                        data=json.dumps(sample_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"registered successfully", response.data)

    def test_user_signup_missing_info(self):
        response = self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                        data=json.dumps({"email": "admin@otheradmin.com",
                                        "password": "adminpassword"}))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"check your inputs", response.data)

    def test_user_signup_empty_fields(self):
        response = self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                        data=json.dumps({"name": "","email": "notadmin@admin.com",
                                        "password": "adminpassword", "rights": ''}))
        self.assertEquals(response.status_code, 400)
        self.assertIn(b"Invalid request/input", response.data)

    def test_invalid_email(self):
        response = self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                        data=json.dumps({"name": "henry tom","email": "adminotheradmincom",
                                        "password": "adminpassword", "rights": 't'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email adress", response.data)

    def test_duplicate_email(self):
        self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                                        data=json.dumps(sample_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"already exists", response.data)

    def test_user_login(self):
        self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                        data=json.dumps({"email":"admin@trueadmin.com", "password": "adminpassword"}))
        self.assertEqual(response.status_code, 200)

    def test_wrong_login_email(self):
        self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                        data=json.dumps({'email': 'some@email.com', 'password': 'adminpassword'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wrong email address", response.data)

    def test_wrong_login_password(self):
        self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                        data=json.dumps({'email': 'admin@trueadmin.com', 'password': 'badpassword'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wrong password", response.data)

    def test_no_login_values(self):
        self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                        data=json.dumps({'email': '', 'password': ''}))
        self.assertEquals(response.status_code, 400)
        self.assertIn(b"Invalid request/input", response.data)

    def test_no_login_field(self):
        self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/login', content_type="application/json",
                                        data=json.dumps({'email': 'admin@trueadmin.com'}))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"check your inputs", response.data)

    def test_get_all_users(self):
        response = self.testclient.get('/store-manager/api/v1/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Users", response.data)

    def test_get_user_by_email(self):
        self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.get('/store-manager/api/v1/users/admin@trueadmin.com')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"admin@trueadmin.com", response.data)

    def test_get_user_by_id(self):
        self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.get('/store-manager/api/v1/users/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"admin@trueadmin.com", response.data)

    def test_get_user_not_found(self):
        response = self.testclient.get('/store-manager/api/v1/users/email')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Information could not be found", response.data)

    def test_delete(self):
        self.testclient.post('/store-manager/api/v1/auth/signup', content_type="application/json",
                             data=json.dumps(sample_user))
        response = self.testclient.delete('/store-manager/api/v1/users/admin@trueadmin.com')
        self.assertEqual(response.status_code, 202)
        self.assertIn(b"User has been deleted", response.data)

    def test_delete_not_found(self):
        response = self.testclient.delete('/store-manager/api/v1/users/email')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"User with email 'email' not found", response.data)

    def tearDown(self):
        database_cls = Database()
        database_cls.drop_table("DROP TABLE users")