from flask_restful import Resource, reqparse, fields, marshal_with
import data as data
from resources.competency import competency_fields
from resources.area import area_fields

profession_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'area': fields.Nested(area_fields),
    'competencies': fields.Nested(competency_fields)
}

prof_parser = reqparse.RequestParser()\
    .add_argument('name', type=str)\
    .add_argument('area', type=int)\
    .add_argument('competencies', type=int, action='append')


class ProfessionList(Resource):
    @marshal_with(profession_fields)
    def get(self):
        return data.list_professions()

    @marshal_with(profession_fields)
    def post(self):
        args = prof_parser.parse_args()
        return data.add_profession(args.name, args.area, args.competencies)


change_prof_parser = reqparse.RequestParser()\
    .add_argument('added', type=int, action='append')\
    .add_argument('deleted', type=int, action='append')


class Profession(Resource):
    @marshal_with(profession_fields)
    def get(self, prof_id: int):
        return data.get_profession(prof_id)

    @marshal_with(profession_fields)
    def put(self, prof_id: int):
        args = change_prof_parser.parse_args()
        return data.change_profession(prof_id, **args)
