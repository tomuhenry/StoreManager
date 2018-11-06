import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash


class Database:

    def __init__(self):

        self.db_parameters = """dbname='storemanagerdb' user='postgres' 
                                password='challenge3'"""

        self.conn = psycopg2.connect(self.db_parameters)
        self.curs = self.conn.cursor(cursor_factory=RealDictCursor)
        self.admin_pass = generate_password_hash('adminpass')
        self.user_pass = generate_password_hash('userpass')

    def create_tables(self):

        create_commands = (
            """ CREATE TABLE IF NOT EXISTS users(
                user_id serial PRIMARY KEY,
                name VARCHAR(80) NOT NULL,
                email VARCHAR(80) UNIQUE,
                password VARCHAR(300) NOT NULL,
                rights BOOLEAN DEFAULT FALSE
                )""",
            
            """ CREATE TABLE IF NOT EXISTS category(
                category_id serial PRIMARY KEY,
                category_name VARCHAR(80) NOT NULL
                )""",

            """ CREATE TABLE IF NOT EXISTS products(
                product_id serial PRIMARY KEY,
                product_name VARCHAR(100) NOT NULL,
                product_specs VARCHAR(50),
                product_price INT NOT NULL,
                product_stock INT NOT NULL,
                category_type INTEGER REFERENCES category(category_id) 
                ON DELETE CASCADE
                )""",

            """ CREATE TABLE IF NOT EXISTS sales(
                sale_id serial PRIMARY KEY,
                sale_quantity INT NOT NULL,
                sale_price INTEGER,
                date_sold DATE,
                product_sold INTEGER REFERENCES products(product_id)
                ON DELETE CASCADE
                )""",

            """ INSERT INTO users(name, email, password, rights)
                SELECT * FROM (
                    SELECT 'Tomu Henry', 'admin@admin.com', '{0}' , TRUE)
                AS tmp WHERE NOT EXISTS(SELECT email FROM users
                WHERE email = 'admin@admin.com')
                LIMIT 1;""".format(self.admin_pass),

            """ INSERT INTO users(name, email, password, rights)
                SELECT * FROM (
                    SELECT 'Not Admin', 'notadmin@notadmin.com', '{0}' , FALSE)
                AS tmp WHERE NOT EXISTS(SELECT email FROM users
                WHERE email = 'notadmin@notadmin.com')
                LIMIT 1;""".format(self.user_pass)

        )

        for command in create_commands:
            self.curs.execute(command)

        self.conn.commit()

    def sql_insert(self, sql_queries, information):
        self.sql_queries = sql_queries
        self.information = information
        self.curs.execute(sql_queries, information)
        self.conn.commit()

    def sql_fetch_all(self, sql_queries):
        self.sql_queries = sql_queries
        self.curs.execute(sql_queries)
        fetched = self.curs.fetchall()
        return fetched

    def sql_fetch_one(self, sql_queries):
        self.sql_queries = sql_queries
        self.curs.execute(sql_queries)
        fetched = self.curs.fetchone()
        return fetched

    def execute_query(self, sql_queries):
        self.sql_queries = sql_queries
        self.curs.execute(sql_queries)
        self.conn.commit()

    @staticmethod
    def drop_table(command):
        db_parameters = """dbname='storemanagerdb' user='postgres' password='challenge3'"""
        conn = psycopg2.connect(db_parameters)
        curs = conn.cursor()
        curs.execute(command)
        conn.commit()
        conn.close()
