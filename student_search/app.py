import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.student import Student, Students
from resources.user import UserRegister
from resources.degree import Degree, Degrees
from security import authenticate, identity

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "testing"
api = Api(app)

# create /auth endpoint
# call authenticate to return jwt token if password matches
# use jwt token to get user
jst = JWT(app, authenticate, identity)

api.add_resource(Student, "/student/<string:id>")
api.add_resource(Degree, "/degree/<string:name>")
api.add_resource(Students, "/students")
api.add_resource(Degrees, "/degrees")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
