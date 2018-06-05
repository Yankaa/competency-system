from flask import Flask
from flask_restful import Api
from resources.competency import CompetencyList, Competency
from resources.profession import ProfessionList, Profession
from resources.area import AreaList, Area
from resources.clusterizer import ClustersUpdate
import data as data

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
data.db.init_app(app)

# with app.app_context():
#     data.create_bd()

api.add_resource(CompetencyList, '/competencies')
api.add_resource(Competency, '/competencies/<int:comp_id>')
api.add_resource(ProfessionList, '/professions')
api.add_resource(Profession, '/professions/<int:prof_id>')
api.add_resource(AreaList, '/areas')
api.add_resource(Area, '/areas/<int:area_id>')
api.add_resource(ClustersUpdate, '/clusters_update')


if __name__ == '__main__':
    app.run(port=5001)
