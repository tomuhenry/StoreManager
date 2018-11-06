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

    def get_all_sales(self):
        get_sales = """SELECT * FROM sales"""
        return self.database_cls.sql_fetch_all(get_sales)

    def get_sale_by_id(self, sale_id):
        get_one_sale = """SELECT * FROM sales WHERE sale_id = {0}""".format(
            sale_id)
        return self.database_cls.sql_fetch_one(get_one_sale)

    def get_sales_by_product_id(self, product_id):
        get_prod_sale = """SELECT * FROM sales WHERE product_sold = {0}""".format(
            product_id)
        return self.database_cls.sql_fetch_all(get_prod_sale)
