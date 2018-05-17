from flask_restful import Resource, reqparse, fields, marshal_with
import data
import model

worker_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'competencies': fields.List(fields.Integer)
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('competencies', type=int, action='append')


class WorkerList(Resource):
    @marshal_with(worker_fields)
    def get(self):
        return data.list_workers()

    @marshal_with(worker_fields)
    def post(self):
        args = parser.parse_args()
        worker = data.add_worker(args.name, args.competencies)
        return worker


class Worker(Resource):
    @marshal_with(worker_fields)
    def get(self, worker_id: int):
        return data.get_worker(worker_id)

    @marshal_with(worker_fields)
    def put(self, worker_id: int):
        args = parser.parse_args()
        return data.change_worker(worker_id, **args)


class DemandedCompetencies(Resource):
    def get(self, worker_id: int):
        return model.demanded_competencies(data.get_worker(worker_id))


class GlobalDemandedCompetencies(Resource):
    def get(self):
        return model.global_demanded_competencies()


class BestWorkers(Resource):
    @marshal_with(worker_fields)
    def get(self, work_id: int):
        return model.best_workers(data.get_work(work_id))
