from database.database import Database


class Products:
    def __init__(self):
        self.database_cls = Database()
        self.database_cls.create_tables()

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

    def get_category_by_name(self, category_name):
        get_category = """ SELECT * FROM category 
                WHERE category_name = '{0}' """.format(category_name)
        return self.database_cls.sql_fetch_all(get_category)

    def get_all_categories(self):
        get_categories = """ SELECT * FROM category """
        return self.database_cls.sql_fetch_all(get_categories)

    def get_category_by_id(self, category_id):
        get_categories = """ SELECT * FROM category 
                WHERE category_id = {0} """.format(category_id)
        return self.database_cls.sql_fetch_all(get_categories)

    def add_category_to_product(self, product_id, category_type):
        add_to_category = """UPDATE products SET category_type = {1} 
                        WHERE product_id = {0} """.format(
            product_id, category_type)
        return self.database_cls.execute_query(add_to_category)

    def get_products_by_category(self, category_type):
        get_category = " SELECT * FROM products WHERE category_type = {0};".format(
            category_type)
        return self.database_cls.sql_fetch_all(get_category)

    def get_all_products(self):
        get_products = """SELECT * FROM products """
        return self.database_cls.sql_fetch_all(get_products)
