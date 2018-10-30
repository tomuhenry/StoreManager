from api.database.database import Database


class Products():
    def __init__(self):
        self.database_cls = Database()

    def add_product(self, category, product_name, product_specs, product_price, product_stock):
        self.category = category
        self.product_name = product_name
        self.product_specs = product_specs
        self.product_price = product_price
        self.product_stock = product_stock

        insert_product = """INSERT INTO 
                            products(category, product_name, product_specs, 
                            product_price, product_stock) VALUES(%s, %s, %s, %s, %s)"""

        details = (category, product_name, product_specs,
                   product_price, product_stock)

        self.database_cls.sql_insert(insert_product, details)

    @staticmethod
    def get_all_products():
        get_products = """SELECT * FROM products """
        database_cls = Database()
        return database_cls.sql_fetch_all(get_products)
