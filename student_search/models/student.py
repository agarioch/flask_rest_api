import sqlite3


class StudentModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def json(self):
        return {"id": self.id, "name": self.name}

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()

        query = "SELECT * FROM students WHERE id=?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()
        query = "INSERT INTO students VALUES (?, ?)"
        cursor.execute(query, (self.id, self.name))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()
        query = "UPDATE students SET name=? WHERE id=?"
        cursor.execute(query, (self.name, self.id))
        connection.commit()
        connection.close()
