import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash


class Database:

    def __init__(self):
        self.db_parameters = "dbname='storemanagerdb' user='postgres' password='challenge3'"

        try:
            conn = psycopg2.connect(self.db_parameters)
            self.curs = conn.cursor()
            admin_pass = generate_password_hash('adminpass')

            # Create database tables

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
                    category VARCHAR(80) NOT NULL,
                    product_name VARCHAR(100) NOT NULL,
                    product_specs VARCHAR(50) NOT NULL,
                    product_price INT NOT NULL,
                    product_stock INT NOT NULL
                    )""",

                """ CREATE TABLE IF NOT EXISTS sales(
                    sale_id serial PRIMARY KEY,
                    sale_quantity int NOT NULL,
                    sale_price INT,
                    date_sold DATE NOT NULL
                    )""",

                """ INSERT INTO users(name, email, password, rights)
                    SELECT * FROM (SELECT 'Tomu Henry', 'admin@admin.com', '{0}' , TRUE)
                    AS tmp WHERE NOT EXISTS(SELECT email FROM users 
                    WHERE email = 'admin@admin.com')LIMIT 1;""".format(admin_pass)
            )

            for command in create_commands:
                self.curs.execute(command)

            conn.commit()

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)


    def sql_insert(self, sql_queries, information):
        self.sql_queries = sql_queries
        self.information = information

        try:
            conn = psycopg2.connect(self.db_parameters)
            curs = conn.cursor()
            curs.execute(sql_queries, information)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
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

    def sql_delete_item(self, sql_queries):
        self.sql_queries = sql_queries
        conn = psycopg2.connect(self.db_parameters)
        curs = conn.cursor()
        curs.execute(sql_queries)
        conn.commit()
        conn.close()

    def sql_edit_item(self, sql_queries):
        self.sql_queries = sql_queries
        conn = psycopg2.connect(self.db_parameters)
        curs = conn.cursor(cursor_factory=RealDictCursor)
        curs.execute(sql_queries)
        conn.commit()
        conn.close()

    @staticmethod
    def drop_table(command):
        db_parameters = "dbname='storemanagerdb' user='postgres' password='challenge3'"
        conn = psycopg2.connect(db_parameters)
        curs = conn.cursor()
        curs.execute(command)
        conn.commit()
        conn.close()
