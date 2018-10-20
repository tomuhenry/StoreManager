from flask import jsonify, abort
from datetime import datetime

time = str(datetime.now())

products = [{
            "product_id": 1,
            "product_name": "wine",
            "product_specs": "700ml",
            "product_stock": 15,
            "product_price": 15000
        },
        {
            "product_id": 2,
            "product_name": "chicken",
            "product_specs": "1kg",
            "product_stock": 25,
            "product_price": 11000
        }]

sales = [{
            "sale_id": 1,
            "product_id": 1,
            "sale_quantity": 3,
            "unit_price": 15000,
            "sale_price": 45000,
            "date_sold": "2018-10-16 11:40:34"
        }]

users = []


class Products:

    def __init__(self, product_name, product_specs, product_stock, product_price):
        self.product_name = product_name
        self.product_specs = product_specs
        self.product_stock = product_stock
        self.product_price = product_price

    def add_product(self):
        new_product = {
            "product_name": self.product_name,
            "product_specs": self.product_specs,
            "product_stock": int(self.product_stock),
            "product_price": int(self.product_price),
        }

        for product in products:
            if set(new_product.values()).issubset(product.values()):
                return False

        else:
            new_product["product_id"] = products[-1]['product_id']+1
            products.append(new_product)
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

class Users:

    def __init__(self, email, name, password, rights):
        self.email = email
        self.name = name
        self.password = password
        self.rights = rights

    def add_user(self):
        if len(users) is 0:
            user_id = 1
            return user_id
        else:
            user_id = users[-1]['user_id']+1
            return user_id

        user = {
                'user_id': user_id,
                'email': self.email,
                'name': self.name,
                'passowrd': self.password,
                'rights': self.rights
            }
        users.append(user)
        return users

    # def user_login(self):
    #     for user in users:

