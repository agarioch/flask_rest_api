import sqlite3


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self):
        return "user (id={}, name={}, pw={})".format(
            self.id, self.username, self.password
        )

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user
