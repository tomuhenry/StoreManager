from unittest import TestCase
from flask import json
from api import app
from api.database.database import Database

sample_user = {
    "name": "tom1 Admin",
    "email": "admin@trueadmin.com",
    "password": "adminpassword",
    "rights": 'false'
}
sample_user_login = {
    "email": "admin@trueadmin.com",
    "password": "adminpassword"
}
database_cls = Database()


class UserTestCase(TestCase):

    def setUp(self):
        database_cls.create_tables()
        self.headers = {'Content-Type': "application/json"}
        self.testclient = app.test_client()
        response_admin = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                              data=json.dumps({'email': 'admin@admin.com', 'password': 'adminpass'}))
        self.access_token1 = json.loads(response_admin.data)['access_token']
        response_user = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                             data=json.dumps({'email': 'notadmin@notadmin.com', 'password': 'userpass'}))
        self.access_token2 = json.loads(response_user.data)['access_token']

    def test_unauthorized_access(self):
        response = self.testclient.post('/store-manager/api/v1/auth/signup',
                                        data=json.dumps(sample_user))
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Missing Authorization Header", response.data)

    def test_user_signup(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                                        data=json.dumps(sample_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"registered successfully", response.data)

    def test_user_signup_unathorized(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                                        data=json.dumps(sample_user))
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"You're not Authorized to add user", response.data)

    def test_user_signup_missing_info(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                                        data=json.dumps({"email": "admin@otheradmin.com",
                                                         "password": "adminpassword"}))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"check your inputs", response.data)

    def test_user_signup_empty_fields(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                                        data=json.dumps({"name": "", "email": "notadmin@admin.com",
                                                         "password": "adminpassword", "rights": ''}))
        self.assertEquals(response.status_code, 400)
        self.assertIn(b"Invalid request/input", response.data)

    def test_invalid_email(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                                        data=json.dumps({"name": "henry tom", "email": "adminotheradmincom",
                                                         "password": "adminpassword", "rights": 't'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email address", response.data)

    def test_duplicate_email(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                                        data=json.dumps(sample_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"already exists", response.data)

    def test_user_login(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                             data=json.dumps(sample_user))
        self.headers = {'Content-Type': "application/json"}
        response = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                        data=json.dumps(sample_user_login))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"access_token", response.data)

    def test_unauthrized_access(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                        data=json.dumps(
                                            {"email": "admin@trueadmin.com",
                                             "password": "adminpassword"}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"access_token", response.data)

    def test_wrong_login_email(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                        data=json.dumps({'email': 'some@email.com', 'password': 'adminpassword'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wrong email address", response.data)

    def test_wrong_login_password(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                        data=json.dumps({'email': 'admin@trueadmin.com', 'password': 'badpassword'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wrong password", response.data)

    def test_no_login_values(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                        data=json.dumps({'email': '', 'password': ''}))
        self.assertEquals(response.status_code, 400)
        self.assertIn(b"Invalid request/input", response.data)

    def test_no_login_field(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                             data=json.dumps(sample_user))
        response = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                        data=json.dumps({'email': 'admin@trueadmin.com'}))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"check your inputs", response.data)

    def test_get_all_users(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.get(
            '/store-manager/api/v1/users', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Users", response.data)

    def test_get_all_users_unauthorized(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.get(
            '/store-manager/api/v1/users', headers=self.headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            b"You're not Authorized to perform action", response.data)

    def test_get_user_by_email(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                             data=json.dumps(sample_user))
        response = self.testclient.get(
            '/store-manager/api/v1/users/admin@trueadmin.com', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"admin@trueadmin.com", response.data)

    def test_get_user_by_id(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.get(
            '/store-manager/api/v1/users/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user_id", response.data)

    def test_get_user_not_found(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.get(
            '/store-manager/api/v1/users/email', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Information could not be found", response.data)

    def test_delete(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                             data=json.dumps(sample_user))
        response = self.testclient.delete(
            '/store-manager/api/v1/users/admin@trueadmin.com', headers=self.headers)
        self.assertEqual(response.status_code, 202)
        self.assertIn(b"User has been deleted", response.data)

    def test_delete_not_found(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.delete(
            '/store-manager/api/v1/users/email', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"User with email 'email' not found", response.data)

    def test_edit_user(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/auth/signup', headers=self.headers,
                             data=json.dumps(sample_user))
        response = self.testclient.put('/store-manager/api/v1/users/2', headers=self.headers,
                                       data=json.dumps({"rights": "true"}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User Rights have been changed", response.data)

    def tearDown(self):
        database_cls.drop_table("DROP TABLE users")
        database_cls.create_tables()
