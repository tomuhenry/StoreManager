from tests import BaseTestCase
from flask import json
from api import app
app.config['TESTING'] = True

sample_product = {
    "product_name": "Knife set",
    "product_specs": "5 pcs",
    "product_stock": 100,
    "product_price": 11500
}


class CategoryTestCase(BaseTestCase):

    def setUp(self):
        self.headers = {'Content-Type': "application/json"}
        self.testclient = app.test_client()
        response_admin = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                              data=json.dumps({'email': 'admin@admin.com', 'password': 'adminpass'}))
        self.access_token1 = json.loads(response_admin.data)['admin_token']
        response_user = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                             data=json.dumps({'email': 'notadmin@notadmin.com', 'password': 'userpass'}))
        self.access_token2 = json.loads(response_user.data)['user_token']

    def test_add_new_category(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.post('/store-manager/api/v1/category', headers=self.headers,
                                        data=json.dumps({"category_name": "Electronics"}))
        self.assertEquals(response.status_code, 201)
        self.assertIn(
            b"New Category 'Electronics' created successfully", response.data)

    def test_add_duplicate_category(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/category', headers=self.headers,
                             data=json.dumps({"category_name": "Electronics"}))
        response = self.testclient.post('/store-manager/api/v1/category', headers=self.headers,
                                        data=json.dumps({"category_name": "Electronics"}))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"Category already exists", response.data)

    def test_add_new_category_unauthorized(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.post('/store-manager/api/v1/category', headers=self.headers,
                                        data=json.dumps({"category_name": "Electronics"}))
        self.assertEquals(response.status_code, 401)
        self.assertIn(b"Only Admin can perform this action", response.data)

    def test_get_all_categories(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/category', headers=self.headers,
                                        data=json.dumps({"category_name": "Electronics"}))
        response = self.testclient.get(
            '/store-manager/api/v1/category', headers=self.headers)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"category_name", response.data)

    def test_get_all_categories_unauthorized(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.get(
            '/store-manager/api/v1/category', headers=self.headers)
        self.assertEquals(response.status_code, 401)
        self.assertIn(b"Only Admin can perform this action", response.data)

    def test_get_category_by_id(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.post('/store-manager/api/v1/category', headers=self.headers,
                                        data=json.dumps({"category_name": "Electronics"}))
        response = self.testclient.get(
            '/store-manager/api/v1/category/1', headers=self.headers)
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"category_name", response.data)

    def test_get_category_by_id_not_found(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.get(
            '/store-manager/api/v1/category/1', headers=self.headers)
        self.assertEquals(response.status_code, 404)
        self.assertIn(b"The category was not found", response.data)

    def test_add_category_to_product(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/admin/products', headers=self.headers,
                             data=json.dumps(sample_product))
        self.testclient.post('/store-manager/api/v1/category', headers=self.headers,
                             data=json.dumps({"category_name": "Electronics"}))
        response = self.testclient.put('/store-manager/api/v1/products/category/1', headers=self.headers,
                                       data=json.dumps({"category_type": 1}))
        self.assertEquals(response.status_code, 200)
        self.assertIn(
            b"The product has been added to the category", response.data)

    def test_add_category_to_product_unauthorized(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/admin/products', headers=self.headers,
                             data=json.dumps(sample_product))
        self.testclient.post('/store-manager/api/v1/category', headers=self.headers,
                             data=json.dumps({"category_name": "Electronics"}))
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.put('/store-manager/api/v1/products/category/1', headers=self.headers,
                                       data=json.dumps({"category_type": 1}))
        self.assertEquals(response.status_code, 401)
        self.assertIn(b"Only Admin can perform this action", response.data)

    def test_add_category_to_product_not_found(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/category', headers=self.headers,
                             data=json.dumps({"category_name": "Electronics"}))
        response = self.testclient.put('/store-manager/api/v1/products/category/1', headers=self.headers,
                                       data=json.dumps({"category_type": 1}))
        self.assertEquals(response.status_code, 404)
        self.assertIn(b"The product was not found", response.data)

    def test_get_products_by_category(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/category', headers=self.headers,
                             data=json.dumps({"category_name": "Electronics"}))
        response = self.testclient.get(
            '/store-manager/api/v1/products/category/1', headers=self.headers)
        self.assertEquals(response.status_code, 200) 

    def test_get_products_by_category_not_found(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.get(
            '/store-manager/api/v1/products/category/1', headers=self.headers)
        self.assertEquals(response.status_code, 404)
        self.assertIn(b"The category was not found", response.data)

    def test_get_products_by_category_unauthorized(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.get(
            '/store-manager/api/v1/products/category/1', headers=self.headers)
        self.assertEquals(response.status_code, 401)
        self.assertIn(b"Only Admin can perform this action", response.data)
