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
        print(student)

        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()
        query = "INSERT INTO students VALUES (?, ?)"
        cursor.execute(query, (student["id"], student["name"]))
        connection.commit()
        connection.close()

        return student, 201

    @jwt_required()
    def delete(self, id):
        global students
        students = [student for student in students if student["id"] != id]
        return {"message": "Student deleted"}

    @jwt_required()
    def put(self, id):
        data = Student.parser.parse_args()
        student = next((student for student in students if student["id"] == id), None)
        if student is None:
            student = {"id": id, "name": data["name"]}
            students.append(student)
        else:
            student.update(data)
        return student


class Students(Resource):
    @jwt_required()
    def get(self):
        if students:
            return {"students": students}
        return {"students": None}, 404
