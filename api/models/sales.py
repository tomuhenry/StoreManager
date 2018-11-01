from api.database.database import Database

class Sales:
    def __init__(self):
        self.database_cls = Database()

    def make_a_sale(self, sale_quantity, sale_price, date_sold, product_sold):
        self.sale_quantity = sale_quantity
        self.sale_price = sale_price
        self.date_sold = date_sold
        self.product_sold = product_sold

        insert_sale = """INSERT INTO
                            sales(sale_quantity, sale_price, date_sold,
                            product_sold) VALUES(%s, %s, %s, %s)"""

        details = (sale_quantity, sale_price, date_sold, product_sold)

        self.database_cls.sql_insert(insert_sale, details)