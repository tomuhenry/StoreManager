from flask import jsonify, abort
from datetime import datetime
import re

time = str(datetime.now())

products =[]
sales = []
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
            products.append(new_product)

            if len(products) is 1:
                products[0]['product_id'] = 1

            else:
                products[-1]["product_id"] = products[-2]['product_id']+1
            
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
                "product_id": self.product_id,
                "sale_quantity": self.sale_quantity,
                "unit_price": self.unit_price,
                "sale_price": self.unit_price * self.sale_quantity,
                "date_sold": time
            }
            sales.append(sale)
            if len(sales) is 1:
                sales[0]['sale_id'] = 1

            else:
                sales[-1]["sale_id"] = sales[-2]["sale_id"]+1
                
            return True


class Users:

    def __init__(self, email, name, password, rights):
        self.email = email
        self.name = name
        self.password = password
        self.rights = rights

    def validate_email(self):
        in_email = re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email)

        if len(self.email) < 7 or in_email is None:
            return False

        else:
            return True

    def check_duplicate(self):
        for user in users:
            if (self.email in user.values()):
                return False

    def add_user(self):

        new_user = {
        'email': self.email,
        'name': self.name,
        'password': self.password,
        'rights': self.rights
        }
        
        users.append(new_user)

        if len(users) is 1:
            users[0]['user_id'] = 1

        else:
            users[-1]['user_id'] = users[-2]['user_id']+1


    def user_login(self):
        for user in users:
            if self.email in user.values() and self.password in user.values():
                return True

            else:
                return False
