from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "testing"
api = Api(app)

# create /auth endpoint
# call authenticate to return jwt token if password matches
# use jwt token to get user
jst = JWT(app, authenticate, identity)

students = []


class Student(Resource):
    @jwt_required()
    def get(self, id):
        student = next((student for student in students if student["id"] == id), None)
        if student:
            return student, 200
        return {"message": "student not found"}, 404

    @jwt_required()
    def post(self, id):
        if (
            next((student for student in students if student["id"] == id), None)
            is not None
        ):
            return {"message": "A student with id {} already exists".format(id)}, 400
        request_data = request.get_json()
        student = {"id": id, "name": request_data["name"]}
        students.append(student)
        return student, 201

    @jwt_required()
    def delete(self, id):
        global students
        students = [student for student in students if student["id"] != id]
        return {"message": "Student deleted"}

    @jwt_required()
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "name", type=str, required=True, help="this field cannot be left blank"
        )
        data = parser.parse_args()
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


api.add_resource(Student, "/student/<string:id>")
api.add_resource(Students, "/students")

app.run(port=5000, debug=True)
