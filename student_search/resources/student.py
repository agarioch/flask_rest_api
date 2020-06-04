import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.student import StudentModel


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="this field cannot be left blank"
    )
    parser.add_argument(
        "degree_id", type=int, required=True, help="please provide degree id"
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
        student = StudentModel(id, **data)

        try:
            student.save_to_db()
        except:
            return {"message", "An error occured creating the student."}, 500

        return student.json(), 201

    @jwt_required()
    def delete(self, id):
        student = StudentModel.find_by_id(id)
        if student:
            student.delete_from_db()
        return {"message": "Student deleted"}

    @jwt_required()
    def put(self, id):
        data = Student.parser.parse_args()
        student = StudentModel.find_by_id(id)

        if student is None:
            student = StudentModel(id, **data)
        else:
            student.name = data["name"]
            student.degree_id = data["degree_id"]

        student.save_to_db()

        return student.json(), 201


class Students(Resource):
    @jwt_required()
    def get(self):
        return {"Students": [student.json() for student in StudentModel.query.all()]}
