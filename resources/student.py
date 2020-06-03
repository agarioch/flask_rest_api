import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.student import StudentModel


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="this field cannot be left blank"
    )

    @jwt_required()
    def get(self, id):
        student = StudentModel.find_by_id(id)
        if student:
            return student.json()
        return {"message": "student not found"}, 404

    @jwt_required()
    def post(self, id):
        if StudentModel.find_by_id(id):
            return {"message": "A student with id {} already exists".format(id)}, 400

        data = Student.parser.parse_args()
        student = StudentModel(id, data["name"])

        try:
            student.insert()
        except:
            return {"message", "An error occured creating the student."}, 500

        return student.json(), 201

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
        student = StudentModel.find_by_id(id)
        updated_student = StudentModel(id, data["name"])
        if student is None:
            try:
                updated_student.insert()
            except:
                return {"message": "An error occurred creating the student."}, 500
        else:
            try:
                updated_student.update()
            except:
                return {"message": "An error occured updating the student."}, 500
        return student.json(), 201


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
