from api.database.database import Database


class Products:
    def __init__(self):
        self.database_cls = Database()

    def add_product(self, **kwargs):
        self.product_name = kwargs.get('product_name')
        self.product_specs = kwargs.get('product_specs')
        self.product_price = kwargs.get('product_price')
        self.product_stock = kwargs.get('product_stock')

        insert_product = """INSERT INTO
                            products(product_name, product_specs, 
                            product_price, product_stock) VALUES(%s, %s, %s, %s)"""

        details = (self.product_name, self.product_specs,
                   self.product_price, self.product_stock)

        self.database_cls.sql_insert(insert_product, details)

    def get_one_product_by_id(self, product_id):

        get_one_product = " SELECT * FROM products WHERE product_id = {0}; ".format(
            product_id)
        return self.database_cls.sql_fetch_one(get_one_product)

    def delete_a_product(self, product_id):
        delete_product = "DELETE FROM products WHERE product_id = {0} ".format(
            product_id)
        return self.database_cls.execute_query(delete_product)

    def edit_a_product(self, product_id, product_name, product_stock, product_price):
        edit_product = """UPDATE products SET product_name = '{1}', product_stock = {2}, 
            product_price = {3} WHERE product_id = {0} """.format(
            product_id, product_name, product_stock, product_price)
        return self.database_cls.execute_query(edit_product)

    def check_same_product(self, product_name, product_specs):
        same_product = """ SELECT * FROM products WHERE product_name = '{0}' AND
                    product_specs = '{1}'""".format(product_name, product_specs)
        return self.database_cls.sql_fetch_all(same_product)

    def create_category(self, category_name):
        add_category = """ INSERT INTO category(category_name) VALUES(%s) """
        details = (category_name,)
        return self.database_cls.sql_insert(add_category, details)

    def add_product_to_category(self, product_id, category_id):
        add_to_category = """ INSERT INTO
                            category(product_id) VALUES(%s) WHERE category_id = {0} """.format(category_id)
        details = (category_id,)
        return self.database_cls.sql_insert(add_to_category, details)

    def get_products_by_category(self, category_name):
        get_category = " SELECT * FROM category WHERE category_name = '{0}';".format(
            category_name)
        return self.database_cls.sql_fetch_all(get_category)

    @staticmethod
    def get_all_products():
        database_cls = Database()
        get_products = """SELECT * FROM products """
        return database_cls.sql_fetch_all(get_products)
