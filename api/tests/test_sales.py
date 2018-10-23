from unittest import TestCase
from flask import json
from api.endpoints.app import app
from api.tests.test_products import sample_product

sample_sale = {
    "product_id": 1,
    "sale_quantity": 25
}
sample_sale2 = {
    "product_id": 1,
    "sale_quantity": 45
}


class SalesTestCase(TestCase):

    def setUp(self):
        self.testclient = app.test_client()
        self.testclient.post('/store-manager/api/v1/admin/products', content_type="application/json",
                             data=json.dumps(sample_product))

    def test_add_sale(self):
        response = self.testclient.post('/store-manager/api/v1/user/sales', content_type="application/json",
                                        data=json.dumps(sample_sale))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The sale item has been added", response.data)

    def test_sale_more_than_stock(self):
        response = self.testclient.post('/store-manager/api/v1/user/sales', content_type="application/json",
                                        data=json.dumps(sample_sale2))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Out of Stock", response.data)

    def test_invalid_sale_report_input_type(self):
        response = self.testclient.post('/store-manager/api/v1/user/sales', content_type="application/json",
                                        data=json.dumps({
                                            "product_id": 1,
                                            "sale_quantity": "25"}))
        self.assertRaises(TypeError)
        self.assertIn(b"Wrong input type", response.data)

    def test_sale_with_wrong_product_id(self):
        response = self.testclient.post('/store-manager/api/v1/user/sales', content_type="application/json",
                                        data=json.dumps({
                                            "product_id": "2t",
                                            "sale_quantity": 25}))
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Not found", response.data)

    def test_get_all_sales(self):
        response = self.testclient.get('/store-manager/api/v1/admin/sales')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sales", response.data)

    def test_get_specific_sale(self):
        self.testclient.post('/store-manager/api/v1/admin/sales', content_type="application/json",
                             data=json.dumps(sample_sale))
        response = self.testclient.get('/store-manager/api/v1/admin/sales/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sale", response.data)

    def test_sale_not_found(self):
        response = self.testclient.get('/store-manager/api/v1/admin/sales/10')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Not found", response.data)
