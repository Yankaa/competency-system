from flask import Flask
from flask_restful import Api
from resources.work import Work, WorkList, BestWorks, EmployerWorks
from resources.worker import Worker, WorkerList, DemandedCompetencies, GlobalDemandedCompetencies, BestWorkers
from resources.employer import Employer, EmployerList
import data
import model

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
with app.app_context():
    data.db.init_app(app)
    # data.create_bd()
    model.init()

api.add_resource(WorkList, '/works')
api.add_resource(Work, '/works/<int:work_id>')
api.add_resource(WorkerList, '/workers')
api.add_resource(Worker, '/workers/<int:worker_id>')
api.add_resource(EmployerList, '/employers')
api.add_resource(Employer, '/employers/<int:employer_id>')
api.add_resource(DemandedCompetencies, '/demanded_competencies/<int:worker_id>')
api.add_resource(GlobalDemandedCompetencies, '/demanded_competencies')
api.add_resource(BestWorks, '/best_works/<int:worker_id>')
api.add_resource(BestWorkers, '/best_workers/<int:work_id>')
api.add_resource(EmployerWorks, '/employer_works/<int:employer_id>')


if __name__ == '__main__':
    app.run(port=5002)
