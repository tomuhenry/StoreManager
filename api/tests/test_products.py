from unittest import TestCase
from flask import json
from api.endpoints.app import app
from api.endpoints.functions import Sales, Products

sample_product = {
    "product_category": "drinks",
    "product_name": "water",
    "product_specs": "500ml",
    "product_stock": 425,
    "product_price": 1000
}
edit_product = {
	"product_stock": 25,
    "product_price": 1200
}


class ProductsTestCase(TestCase):

    def setUp(self):
        self.testclient = app.test_client()

    def test_home_route(self):
        response = self.testclient.get('/store-manager/api/v1/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Store manager api", response.data)

    def test_add_product(self):
        response = self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                                        data=json.dumps(sample_product))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The product has been added", response.data)

    def test_added_product_there(self):
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                                data=json.dumps(sample_product))
        response = self.testclient.get('/store-manager/api/v1/admin/products/3')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"500ml", response.data)

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
        self.assertEquals(response.status_code, 500)
        self.assertIn(b"Server Error has occured, Check input", response.data)

    def test_get_all_products(self):
        response = self.testclient.get('/store-manager/api/v1/admin/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products", response.data)

    def test_get_one_product(self):
        response = self.testclient.get('/store-manager/api/v1/admin/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product", response.data)

    def test_get_one_product_not_found(self):
        response = self.testclient.get('/store-manager/api/v1/admin/products/10')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Not found", response.data)

    def test_edit_product(self):
        response = self.testclient.put('/store-manager/api/v1/admin/products/1', content_type="application/json",
                                        data=json.dumps(edit_product))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"Updated", response.data)

    def test_edit_product_not_found(self):
        response = self.testclient.put('/store-manager/api/v1/admin/products/10', content_type="application/json",
                                        data=json.dumps(edit_product))
        self.assertEquals(response.status_code, 500)
        self.assertIn(b"Server Error", response.data)
        
    def test_edit_product_wrongly(self):
        response = self.testclient.put('/store-manager/api/v1/admin/products/1', content_type="application/json",
                                        data=json.dumps({"product_price": 1200}))
        self.assertEquals(response.status_code, 500)
        self.assertIn(b"Server Error", response.data)

    def test_delete_product(self):
        response = self.testclient.delete('/store-manager/api/v1/admin/products/2')
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"Deleted", response.data)
    
    def test_delete_product_removed(self):
        response1 = self.testclient.delete('/store-manager/api/v1/admin/products/2')
        response = self.testclient.get('/store-manager/api/v1/admin/products/2')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b"Not found", response.data)

    def test_delete_product_not_found(self):
        response = self.testclient.delete('/store-manager/api/v1/admin/products/10')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b"Not found", response.data)