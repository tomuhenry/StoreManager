from datetime import datetime
import re
import uuid

time = str(datetime.now())

products = []
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
            "product_id": str(uuid.uuid4()),
            "product_name": self.product_name,
            "product_specs": self.product_specs,
            "product_stock": int(self.product_stock),
            "product_price": int(self.product_price),
        }

        products.append(new_product)


class Sales:
    def __init__(self, product_id, sale_quantity, product_price):
        self.product_id = product_id
        self.sale_quantity = sale_quantity
        self.product_price = product_price

    def add_sale(self):

        sale = {
            "sale_id": str(uuid.uuid4()),
            "product_id": self.product_id,
            "sale_quantity": self.sale_quantity,
            "product_price": self.product_price,
            "sale_price": self.product_price * self.sale_quantity,
            "date_sold": time
        }
        sales.append(sale)


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
            'user_id': str(uuid.uuid1()),
            'email': self.email,
            'name': self.name,
            'password': self.password,
            'rights': self.rights
        }

        users.append(new_user)