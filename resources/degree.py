from flask_restful import Resource

from models.degree import DegreeModel


class Degree(Resource):
    def get(self, name):
        degree = DegreeModel.find_by_name(name)
        if degree:
            return degree.json(), 200
        return {"message": "degree not found"}, 404

    def post(self, name):
        if DegreeModel.find_by_name(name):
            return {"message": "A store with name {} already exists".format(name)}, 400
        degree = DegreeModel(name)
        try:
            degree.save_to_db()
        except:
            return {"message": "An error occured while creating the store"}, 500

        return degree.json(), 201

    def delete(self, name):
        degree = DegreeModel.find_by_name(name)
        if degree:
            degree.delete_from_db()
        return {"message": "Degree deleted"}


class Degrees(Resource):
    def get(self):
        return {"degrees": [degree.json() for degree in DegreeModel.query.all()]}
