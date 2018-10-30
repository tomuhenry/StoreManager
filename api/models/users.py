from api.database.database import Database


class Users():

    def add_user(self, name, email, password, rights):
        self.name = name
        self.email = email
        self.password = password
        self.rights = rights
        
        database_cls = Database()

        insert_user = "INSERT INTO users(name, email, password, rights) VALUES(%s, %s, %s, %s)"

        details = (name, email, password, rights)

        database_cls.sql_insert(insert_user, details)
