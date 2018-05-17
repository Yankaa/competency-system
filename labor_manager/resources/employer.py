from flask_restful import Resource, reqparse, fields, marshal_with
import data

employer_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

parser = reqparse.RequestParser()\
    .add_argument('name', type=str)\
    .add_argument('description', type=str)


class EmployerList(Resource):
    @marshal_with(employer_fields)
    def get(self):
        return data.list_employers()

    @marshal_with(employer_fields)
    def post(self):
        args = parser.parse_args()
        employer = data.add_employer(args.name, args.description)
        return employer


class Employer(Resource):
    @marshal_with(employer_fields)
    def get(self, employer_id: int):
        return data.get_employer(employer_id)

    @marshal_with(employer_fields)
    def put(self, employer_id: int):
        args = parser.parse_args()
        return data.change_employer(employer_id, **args)
