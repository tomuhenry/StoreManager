from api.database.database import Database


class Users():

    def add_user(self, name, email, password, rights):
        self.name = name
        self.email = email
        self.password = password
        self.rights = rights

        insert_user = "INSERT INTO users(name, email, password, rights) VALUES(%s, %s, %s, %s)"

        details = (name, email, password, rights)
        
        database_cls = Database()

        database_cls.sql_insert(insert_user, details)


    def login_user(self, email):

        user_logged = "SELECT * FROM users WHERE email = '{0}'".format(email)

        database_cls = Database()

        return database_cls.sql_fetch_one(user_logged)
