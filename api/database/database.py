import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash


class Database:

    def __init__(self):

        self.db_parameters = """dbname='d4eo92qumfels6' user='rydoowkieaxjhf' 
                    password='451025a5501925f1a9c2dad02c65fdd1122b1cc2cfa8d94d021d86e059f74b51' 
                    host = 'ec2-54-83-38-174.compute-1.amazonaws.com'"""
        
        self.admin_pass = generate_password_hash('adminpass')
        self.user_pass = generate_password_hash('userpass')

    def create_tables(self):
        conn = psycopg2.connect(self.db_parameters)
        curs = conn.cursor()
        create_commands = (
            """ CREATE TABLE IF NOT EXISTS users(
                user_id serial PRIMARY KEY,
                name VARCHAR(80) NOT NULL,
                email VARCHAR(80) UNIQUE,
                password VARCHAR(300) NOT NULL,
                rights BOOLEAN DEFAULT FALSE
                )""",

            """ CREATE TABLE IF NOT EXISTS products(
                product_id serial PRIMARY KEY,
                product_name VARCHAR(100) NOT NULL,
                product_specs VARCHAR(50),
                product_price INT NOT NULL,
                product_stock INT NOT NULL
                )""",

            """ CREATE TABLE IF NOT EXISTS sales(
                sale_id serial PRIMARY KEY,
                sale_quantity INT NOT NULL,
                sale_price INTEGER,
                date_sold DATE,
                product_sold INTEGER REFERENCES products(product_id) 
                ON DELETE CASCADE
                )""",
            
            """ CREATE TABLE IF NOT EXISTS category(
                cetegory_id serial PRIMARY KEY,
                product_id INTEGER REFERENCES products(product_id) 
                ON DELETE CASCADE,
                category_name VARCHAR(80) NOT NULL
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
            curs.execute(command)

        conn.commit()
        conn.close()

    def sql_insert(self, sql_queries, information):
        self.sql_queries = sql_queries
        self.information = information
        conn = psycopg2.connect(self.db_parameters)
        curs = conn.cursor(cursor_factory=RealDictCursor)
        curs.execute(sql_queries, information)
        conn.commit()
        conn.close()

    def sql_fetch_all(self, sql_queries):
        self.sql_queries = sql_queries
        conn = psycopg2.connect(self.db_parameters)
        curs = conn.cursor(cursor_factory=RealDictCursor)
        curs.execute(sql_queries)
        fetched = curs.fetchall()
        conn.close()
        return fetched

    def sql_fetch_one(self, sql_queries):
        self.sql_queries = sql_queries
        conn = psycopg2.connect(self.db_parameters)
        curs = conn.cursor(cursor_factory=RealDictCursor)
        curs.execute(sql_queries)
        fetched = curs.fetchone()
        conn.commit()
        conn.close()
        return fetched

    def execute_query(self, sql_queries):
        self.sql_queries = sql_queries
        conn = psycopg2.connect(self.db_parameters)
        curs = conn.cursor(cursor_factory=RealDictCursor)
        curs.execute(sql_queries)
        conn.commit()
        conn.close()

    @staticmethod
    def drop_table(command):

        db_parameters = """dbname='d4eo92qumfels6' user='rydoowkieaxjhf' 
                    password='451025a5501925f1a9c2dad02c65fdd1122b1cc2cfa8d94d021d86e059f74b51' 
                    host = 'ec2-54-83-38-174.compute-1.amazonaws.com'"""
        conn = psycopg2.connect(db_parameters)
        curs = conn.cursor()
        curs.execute(command)
        conn.commit()
        conn.close()
