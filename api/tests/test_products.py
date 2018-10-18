# from tests import BaseTestCase
from unittest import TestCase
from flask import json
from api.app_routes import app

sample_product ={
    "product_category": "drinks",
    "product_name": "water",
    "product_specs": "500ml",
    "product_stock": 425,
    "product_price": 1000
}

class ProductsTestCase(TestCase):

    def setUp(self):
        self.testclient = app.test_client()

    def test_home_route(self):
        pass