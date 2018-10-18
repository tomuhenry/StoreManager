from unittest import TestCase
from flask import json
from api.endpoints.app import app

sample_sale = {
    "product_id": 1,
    "sale_quantity": 25,
    "sale_price": 1500
}

class SalesTestCase(TestCase):
    
    def setUp(self):
        self.testclient = app.test_client()

    def test_add_sale(self):
        response = self.testclient.post('/store-manager/api/v1/user/sales', content_type="application/json",
                                        data=json.dumps(sample_sale))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The sale item has been added", response.data)

    def test_get_all_sales(self):
        response = self.testclient.get('/store-manager/api/v1/admin/sales')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sales", response.data)

    def test_get_specific_sale(self):
        response = self.testclient.get('/store-manager/api/v1/admin/sales/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sale", response.data)