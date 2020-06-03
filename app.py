from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.student import Student, Students

app = Flask(__name__)
app.secret_key = "testing"
api = Api(app)

# create /auth endpoint
# call authenticate to return jwt token if password matches
# use jwt token to get user
jst = JWT(app, authenticate, identity)


api.add_resource(Student, "/student/<string:id>")
api.add_resource(Students, "/students")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
