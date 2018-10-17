from tests import BaseTestCase
import json

new_product = {
    "product_category": "drinks",
    "product_name": "water",
    "product_specs": "500ml",
    "product_stock": 425,
    "product_price": 1000
}

class TestProductsCase(BaseTestCase):

    def test_add_product(self):
        pass