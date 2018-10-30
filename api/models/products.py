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

    def get_one_product_by_id(self, product_id):

        get_one_product = " SELECT * FROM products WHERE product_id = {0}; ".format(
            product_id)
        return self.database_cls.sql_fetch_one(get_one_product)

    def delete_a_product(self, product_id):
        delete_product = "DELETE FROM products WHERE product_id = {0} ".format(
            product_id)
        return self.database_cls.sql_delete_item(delete_product)

    def edit_a_product(self, product_id, product_stock, product_price):
        edit_product = """UPDATE products SET product_stock = {1}, product_price = {2} 
                            WHERE product_id = {0} """.format(
                                product_id, product_stock, product_price)
        return self.database_cls.sql_edit_item(edit_product)

    @staticmethod
    def get_all_products():
        database_cls = Database()
        get_products = """SELECT * FROM products """
        return database_cls.sql_fetch_all(get_products)
