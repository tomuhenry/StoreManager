from tests import BaseTestCase
from flask import json
from api import app
app.config['TESTING'] = True

sample_sale = {
    "sale_quantity": 3,
    "product_sold": 1
}
sample_product = {
    "category": "Kitchen Ware",
    "product_name": "Knife set",
    "product_specs": "5 pcs",
    "product_stock": 100,
    "product_price": 11500
}


class SalesTestCase(BaseTestCase):

    def setUp(self):
        self.headers = {'Content-Type': "application/json"}
        self.testclient = app.test_client()
        response_admin = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                              data=json.dumps({'email': 'admin@admin.com', 'password': 'adminpass'}))
        self.access_token1 = json.loads(response_admin.data)['access_token']
        response_user = self.testclient.post('/store-manager/api/v1/auth/login', headers=self.headers,
                                             data=json.dumps({'email': 'notadmin@notadmin.com', 'password': 'userpass'}))
        self.access_token2 = json.loads(response_user.data)['access_token']
        self.headers['Authorization'] = "Bearer " + self.access_token1
        self.testclient.post('/store-manager/api/v1/admin/products', headers=self.headers,
                             data=json.dumps(sample_product))

    def test_add_sale(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.post('/store-manager/api/v1/sales', headers=self.headers,
                                        data=json.dumps(sample_sale))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"The Sale has been made", response.data)

    def test_add_sale_not_authorized(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.post('/store-manager/api/v1/sales', headers=self.headers,
                                        data=json.dumps(sample_sale))
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Admin cannot make a sale", response.data)

    def test_add_sale_not_found(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.post('/store-manager/api/v1/sales', headers=self.headers,
                                        data=json.dumps({"sale_quantity": 3, "product_sold": 10}))
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"The product has not been found", response.data)

    def test_not_enough_stock(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.post('/store-manager/api/v1/sales', headers=self.headers,
                                        data=json.dumps({"sale_quantity": 200, "product_sold": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Not enough items in stock", response.data)

    def test_view_all_sales(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.get(
            '/store-manager/api/v1/sales', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sales", response.data)

    def test_view_all_sales_not_authorized(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.get(
            '/store-manager/api/v1/sales', headers=self.headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            b"You're not Authorized to perform action", response.data)

    def test_get_one_sale_by_id(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.post('/store-manager/api/v1/sales', headers=self.headers,
                                        data=json.dumps(sample_sale))
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.get(
            '/store-manager/api/v1/sales/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"date_sold", response.data)

    def test_get_one_sale_by_id_not_found(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.get(
            '/store-manager/api/v1/sales/3', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This sale has not been found", response.data)

    def test_get_sales_by_product_id(self):
        self.headers['Authorization'] = "Bearer " + self.access_token2
        response = self.testclient.post('/store-manager/api/v1/sales', headers=self.headers,
                                        data=json.dumps(sample_sale))
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.get(
            '/store-manager/api/v1/sales/products/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"product_sold", response.data)

    def test_get_sales_by_product_id_not_found(self):
        self.headers['Authorization'] = "Bearer " + self.access_token1
        response = self.testclient.get(
            '/store-manager/api/v1/sales/products/5', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"The product hasn't been sold yet", response.data)
