from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_babelex import Babel
from blueprints.competency import competency_page
from blueprints.work import work_page
from blueprints.employer import employer_page
from blueprints.main import main_page
from blueprints.manage_competencies import manage_competencies_page
from blueprints.demanded_competencies import demanded_competencies_page
from blueprints.best_works import best_works_page
import security

app = Flask(__name__)
app.config.from_pyfile('config.py')
babel = Babel(app)
bootstrap = Bootstrap(app)
security.configure(app)
mail = Mail(app)

app.register_blueprint(competency_page)
app.register_blueprint(work_page)
app.register_blueprint(employer_page)
app.register_blueprint(main_page)
app.register_blueprint(manage_competencies_page)
app.register_blueprint(demanded_competencies_page)
app.register_blueprint(best_works_page)


# в comp_table.html требуется проверять наличие элементов в списке
# этот метод преобразует список в словарь, чтобы такие проверки можно было делать эффективно
@app.template_filter('to_set')
def to_set_filter(competencies):
    if competencies is None:
        return None
    return {x['id']: 1 for x in competencies}


if __name__ == '__main__':
    app.run(port=5003)
