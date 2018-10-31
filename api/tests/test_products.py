from unittest import TestCase
from flask import json
from api.views import app
from api.database.database import Database

sample_product = {
    "category": "Kitchen Ware",
    "product_name": "Knife set",
    "product_specs": "5 pcs",
    "product_stock": 100,
    "product_price": 11500
}
edit_product = {
	"product_stock": 25,
    "product_price": 1200
}
wrong_sample_product = {
    "category": "Kitchen Ware",
    "product_name": "Knife set",
    "product_specs": "5 pcs",
    "product_stock": "100O",
    "product_price": "1e500"
}

class ProductsTestCase(TestCase):
    
    def setUp(self):
        database_cls = Database()
        self.testclient = app.test_client()
        

    def test_index_route(self):
        response = self.testclient.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Store manager api", response.data)

    def test_add_product(self):
        response = self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                                        data=json.dumps(sample_product))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"The product has been added", response.data)

    def test_add_product_wrongly(self):
        response = self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                                        data=json.dumps(edit_product))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"A key error has been detected,", response.data)

    def test_add_product_missing_values(self):
        response = self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                                        data=json.dumps({"category": "","product_name": "",
                                        "product_specs": "5 pcs", "product_stock": 100,
                                        "product_price": 11500}))
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
            '/store-manager/api/v1/admin/products/101')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"null", response.data)

    def test_edit_product(self):
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                             data=json.dumps(sample_product))
        response = self.testclient.put('/store-manager/api/v1/admin/products/1', content_type="application/json",
                                       data=json.dumps(edit_product))
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"Product was updated successfully", response.data)

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
        self.assertIn(b"Product was deleted successfully", response.data)

    def test_delete_product_removed(self):
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                             data=json.dumps(sample_product))
        self.testclient.delete('/store-manager/api/v1/admin/products/1')
        response = self.testclient.get(
            '/store-manager/api/v1/admin/products/1')
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"null", response.data)

    def tearDown(self):
        database_cls = Database()
        database_cls.drop_table("DROP TABLE products")
