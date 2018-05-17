from flask_restful import Resource, reqparse, fields, marshal_with
import data
import model
from resources.employer import employer_fields

work_fields = {
    'id': fields.Integer,
    'description': fields.String,
    'salary': fields.Integer,
    'employer': fields.Nested(employer_fields),
    'competencies': fields.List(fields.Integer)
}

parser = reqparse.RequestParser()\
    .add_argument('description', type=str)\
    .add_argument('salary', type=int)\
    .add_argument('employer', type=int)\
    .add_argument('competencies', type=int, action='append')


class WorkList(Resource):
    @marshal_with(work_fields)
    def get(self):
        return data.list_works()

    @marshal_with(work_fields)
    def post(self):
        args = parser.parse_args()
        work = data.add_work(args.description, args.salary, args.employer, args.competencies)
        return work


class Work(Resource):
    @marshal_with(work_fields)
    def get(self, work_id: int):
        return data.get_work(work_id)

    @marshal_with(work_fields)
    def put(self, work_id: int):
        args = parser.parse_args()
        return data.change_work(work_id, **args)


class BestWorks(Resource):
    @marshal_with(work_fields)
    def get(self, worker_id: int):
        return model.best_works(data.get_worker(worker_id))


class EmployerWorks(Resource):
    @marshal_with(work_fields)
    def get(self, employer_id: int):
        return data.employer_works(employer_id)
