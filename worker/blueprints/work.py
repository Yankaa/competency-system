from flask import Blueprint, render_template
from services_info import get_work_info, get_current_user
from blueprints.competency_table import load_table

work_page = Blueprint('work_page', __name__, template_folder='templates')


@work_page.route('/work/<int:work_id>')
def work(work_id: int):
    return render_template("work.html", user=get_current_user(), work=get_work_info(work_id))


@load_table(work_page, '/work/<int:work_id>')
def change_competency(work_id: int):
    return get_work_info(work_id)['competencies']
