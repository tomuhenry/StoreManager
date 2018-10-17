from flask import jsonify, abort
# from data_models import products, sales
from datetime import datetime

time = str(datetime.now())

products = [{
            "product_id": 1,
            "product_category": "drinks",
            "product_name": "wine",
            "product_specs": "700ml",
            "product_stock": 15,
            "product_price": 15000
        }]

sales = [{
            "sale_id": 1,
            "product_id": 1,
            "sale_quantity": 3,
            "unit_price": 15000,
            "sale_price": 45000,
            "date_sold": "2018-10-16 11:40:34"
        }]


class Products:

    def __init__(self, product_category, product_name, product_specs, product_stock, product_price):
        self.product_category = product_category
        self.product_name = product_name
        self.product_specs = product_specs
        self.product_stock = product_stock
        self.product_price = product_price

    def add_product(self):
        product = {
            "product_id": products[-1]['product_id']+1,
            "product_category": self.product_category,
            "product_name": self.product_name,
            "product_specs": self.product_specs,
            "product_stock": self.product_stock,
            "product_price": self.product_price,
        }

        if product in products or [product for product in products
                                   if product["product_category"] == self.product_category and
                                   product["product_name"] == self.product_name and product["product_specs"] == self.product_specs and
                                   product["product_stock"] == self.product_stock and product["product_price"] == self.product_price]:

            return False

        else:
            products.append(product)
            return True


class Sales:
    def __init__(self, product_id, sale_quantity, unit_price):
        self.product_id = product_id
        self.sale_quantity = sale_quantity
        self.unit_price = unit_price

    def add_sale(self):
        product = [
            product for product in products if product["product_id"] == self.product_id]

        if len(product) is 0:
            abort(500)

        "reduce the numer of items in the product list by sold items"
        if self.sale_quantity > product[0]["product_stock"]:
            return False

        else:
            product[0]["product_stock"] = product[0]["product_stock"] - \
                self.sale_quantity

            sale = {
                "sale_id": sales[-1]["sale_id"]+1,
                "product_id": self.product_id,
                "sale_quantity": self.sale_quantity,
                "unit_price": self.unit_price,
                "sale_price": self.unit_price * self.sale_quantity,
                "date_sold": time
            }
            sales.append(sale)
            return True
