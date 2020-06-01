import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="this field cannot be left blank"
    )

    @jwt_required()
    def get(self, id):
        student = self.find_by_id(id)
        if student:
            return student
        return {"message": "student not found"}, 404

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()

        query = "SELECT * FROM students WHERE id=?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"student": {"id": row[0], "name": row[1]}}

    @jwt_required()
    def post(self, id):
        if self.find_by_id(id):
            return {"message": "A student with id {} already exists".format(id)}, 400

        data = Student.parser.parse_args()
        student = {"id": id, "name": data["name"]}

        try:
            self.insert(student)
        except:
            return {"message", "An error occured creating the student."}, 500

        return student, 201

    @classmethod
    def insert(cls, student):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()
        query = "INSERT INTO students VALUES (?, ?)"
        cursor.execute(query, (student["id"], student["name"]))
        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, id):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()
        query = "DELETE FROM students WHERE id=?"
        cursor.execute(query, (id,))
        connection.commit()
        connection.close()
        return {"message": "Student deleted"}

    @jwt_required()
    def put(self, id):
        data = Student.parser.parse_args()
        student = self.find_by_id(id)
        updated_student = {"id": id, "name": data["name"]}
        if student is None:
            try:
                self.insert(updated_student)
            except:
                return {"message": "An error occurred creating the student."}, 500
        else:
            try:
                self.update(updated_student)
            except:
                return {"message": "An error occured updating the student."}, 500
        return student

    @classmethod
    def update(cls, student):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()
        query = "UPDATE students SET name=? WHERE id=?"
        cursor.execute(query, (student["name"], student["id"]))
        connection.commit()
        connection.close()


class Students(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()
        query = "SELECT * FROM students"
        result = cursor.execute(query)
        students = []
        for row in result:
            students.append({"id": row[0], "name": row[1]})
        connection.close()
        if students:
            return students, 200
        return {"students": students}, 404
