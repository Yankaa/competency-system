from flask import Blueprint, render_template
from services_info import get_current_user, get_worker_info
from .competency_table import load_table, get_current_work
from flask_security import login_required

worker_page = Blueprint('worker_page', __name__, template_folder='templates')


@worker_page.route('/worker/<int:worker_id>')
@login_required
def worker(worker_id: int):
    return render_template("worker.html", user=get_worker_info(worker_id), worker=get_worker_info(worker_id),
                           work=get_current_work(from_args=True))


@load_table(worker_page, '/worker/<int:worker_id>')
@login_required
def change_competency(worker_id: int):
    return get_worker_info(worker_id)['competencies']
