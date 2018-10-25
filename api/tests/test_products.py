from unittest import TestCase
from flask import json
from api.views.app import app
from api.views.functions import products

sample_product = {
    "product_name": "water",
    "product_specs": "500ml",
    "product_stock": 25,
    "product_price": 1000
}
edit_product = {
    "product_stock": 25,
    "product_price": 1200
}
missing_edit_product = {
    "product_stock": "",
    "product_price": 1200
}

wrong_sample_product = {
    "product_name": "water",
    "product_specs": "500ml",
    "product_stock": "42m",
    "product_price": 1000
}


class ProductsTestCase(TestCase):

    def setUp(self):
        self.testclient = app.test_client()
        self.products = products

    def test_index_route(self):
        response = self.testclient.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Store manager api", response.data)

    def test_add_product(self):
        response = self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                                        data=json.dumps(sample_product))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The product has been added", response.data)

    def test_duplicate_product(self):
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                             data=json.dumps(sample_product))
        response2 = self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                                         data=json.dumps(sample_product))
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b"The product already exits", response2.data)

    def test_add_product_wrongly(self):
        response = self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                                        data=json.dumps(edit_product))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"A key error has been detected,", response.data)

    def test_add_product_missing_values(self):
        response = self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                                        data=json.dumps({"product_name": "","product_specs": "",
                                        "product_stock": 25,"product_price": 1000}))
        self.assertEquals(response.status_code, 400)
        self.assertIn(b"Invalid request/input", response.data)

    def test_add_product_with_wrong_data_type(self):
        response = self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                                        data=json.dumps(wrong_sample_product))
        self.assertRaises(ValueError)
        self.assertIn(b"Wrong Value in the input", response.data)

    def test_get_all_products(self):
        response = self.testclient.get('/store-manager/api/v1/admin/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products", response.data)

    def test_get_one_product(self):
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                             data=json.dumps(sample_product))
        response = self.testclient.get(
            '/store-manager/api/v1/admin/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product", response.data)

    def test_get_one_product_not_found(self):
        response = self.testclient.get(
            '/store-manager/api/v1/admin/products/10')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Not found", response.data)

    def test_edit_product(self):
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                             data=json.dumps(sample_product))
        response = self.testclient.put('/store-manager/api/v1/admin/products/1', content_type="application/json",
                                       data=json.dumps(edit_product))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"Updated", response.data)

    def test_edit_with_missing_input(self):
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                             data=json.dumps(sample_product))
        response = self.testclient.put('/store-manager/api/v1/admin/products/1', content_type="application/json",
                                       data=json.dumps(missing_edit_product))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"Wrong Value in the input", response.data)

    def test_edit_product_not_found(self):
        response = self.testclient.put('/store-manager/api/v1/admin/products/10', content_type="application/json",
                                       data=json.dumps(edit_product))
        self.assertEquals(response.status_code, 200)
        self.assertIn(
            b"There is not product with ID '10' in the system", response.data)

    def test_edit_product_wrongly(self):
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                             data=json.dumps(sample_product))
        response = self.testclient.put('/store-manager/api/v1/admin/products/1', content_type="application/json",
                                       data=json.dumps({"product_price": 1200}))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"A key error has been detected,", response.data)

    def test_delete_product(self):
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                             data=json.dumps(sample_product))
        response = self.testclient.delete(
            '/store-manager/api/v1/admin/products/1')
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"Deleted", response.data)

    def test_delete_product_removed(self):
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                             data=json.dumps(sample_product))
        self.testclient.delete('/store-manager/api/v1/admin/products/1')
        response = self.testclient.get(
            '/store-manager/api/v1/admin/products/1')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b"Not found", response.data)

    def test_delete_product_not_found(self):
        response = self.testclient.delete(
            '/store-manager/api/v1/admin/products/10')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b"Not found", response.data)

    def tearDown(self):
        self.products.clear()
