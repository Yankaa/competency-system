from flask_restful import Resource, reqparse, fields, marshal_with
import data as data

competency_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'indicators': fields.List(fields.String, attribute=lambda comp: comp.indicators.split('\n'))
}

competency_list_get = reqparse.RequestParser()\
    .add_argument('area', type=int, location='args')\
    .add_argument('profession', type=int, location='args')\
    .add_argument('description', type=str, location='args')

competency_list_post = reqparse.RequestParser()\
    .add_argument('name', type=str)\
    .add_argument('indicators', type=str, action='append')


class CompetencyList(Resource):
    @marshal_with(competency_fields)
    def get(self):
        args = competency_list_get.parse_args()
        return data.list_competencies(args)

    @marshal_with(competency_fields)
    def post(self):
        args = competency_list_post.parse_args()
        return data.add_competency(args.name, args.indicators)


class Competency(Resource):
    @marshal_with(competency_fields)
    def get(self, comp_id: int):
        return data.get_competency(comp_id)
