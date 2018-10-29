import psycopg2


class Database:

    def __init__(self):
        db_parameters = "dbname='storemanagerdb' user='postgres' host='localhost' password='challenge3'"
        try:
            self.conn = psycopg2.connect(db_parameters)
            self.curs = self.conn.cursor()

            # Create database tables

            create_commands = (
                """ CREATE TABLE IF NOT EXISTS users(
                    user_id serial PRIMARY KEY,
                    name VARCHAR(80) UNIQUE,
                    email VARCHAR(80) NOT NULL,
                    password VARCHAR(80) NOT NULL,
                    rights BOOLEAN DEFAULT FALSE
                    )""",
                """ CREATE TABLE IF NOT EXISTS products(
                    product_id serial PRIMARY KEY,
                    category VARCHAR(80) UNIQUE,
                    product_name VARCHAR(100) NOT NULL,
                    product_specs VARCHAR(50) NOT NULL,
                    product_price INT NOT NULL,
                    product_stock INT NOT NULL
                    )""",

                """ CREATE TABLE IF NOT EXISTS sales(
                    user_id serial PRIMARY KEY,
                    name VARCHAR(80) UNIQUE,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(80) NOT NULL,
                    rights VARCHAR(80)
                    )"""
            )

            for command in create_commands:
                self.curs.execute(command)

                self.conn.commit()

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            self.conn.close()


if __name__ == "__main__":
    dbase = Database()
