from flask_restful import Resource, reqparse, fields, marshal_with
import data as data

area_fields = {
    'id': fields.Integer,
    'name': fields.String
}

area_parser = reqparse.RequestParser()\
    .add_argument('name', type=str)


class AreaList(Resource):
    @marshal_with(area_fields)
    def get(self):
        return data.list_areas()

    @marshal_with(area_fields)
    def post(self):
        args = area_parser.parse_args()
        return data.add_area(args.name)


class Area(Resource):
    @marshal_with(area_fields)
    def get(self, area_id: int):
        return data.get_area(area_id)

    @marshal_with(area_fields)
    def put(self, area_id: int):
        args = area_parser.parse_args()
        return data.change_area(area_id, args.name)
