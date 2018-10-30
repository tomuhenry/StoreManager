import psycopg2
from psycopg2.extras import RealDictCursor


class Database:

    def __init__(self):
        self.db_parameters = "dbname='storemanagerdb' user='postgres' host='localhost' password='challenge3'"
        try:
            self.conn = psycopg2.connect(self.db_parameters)
            self.curs = self.conn.cursor()

            # Create database tables

            create_commands = (
                """ CREATE TABLE IF NOT EXISTS users(
                    user_id serial PRIMARY KEY,
                    name VARCHAR(80) NOT NULL,
                    email VARCHAR(80) UNIQUE,
                    password VARCHAR(80) NOT NULL,
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
                    user_id serial PRIMARY KEY,
                    sale_quantity int NOT NULL,
                    sale_price INT,
                    date_sold DATE NOT NULL,
                    product_id FOREIGN KEY,
                    product_price FOREIGN KEY
                    )""",
                """ INSERT INTO users(name, email, password, rights)
                    VALUES('Tomu Henry', 'admin@admin.com', 'adminpass', TRUE)"""
            )

            for command in create_commands:
                self.curs.execute(command)

                self.conn.commit()

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            self.conn.close()


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
            if conn is not None:
                conn.close()

    def sql_fetch_all(self, sql_queries):
        self.sql_queries = sql_queries
        conn = psycopg2.connect(self.db_parameters)
        curs = conn.cursor(cursor_factory=RealDictCursor)
        curs.execute(sql_queries)
        fetched = curs.fetchall()
        conn.close()
        return fetched
            
