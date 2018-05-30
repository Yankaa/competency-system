from flask import Blueprint, render_template
from services_info import get_current_user, get_best_workers
from flask_security import login_required

best_workers_page = Blueprint('best_workers_page', __name__, template_folder='templates')


@best_workers_page.route('/best_workers/<int:work_id>')
@login_required
def best_workers(work_id: int):
    return render_template("best_workers.html", user=get_current_user(), best_workers=get_best_workers(work_id), work_id=work_id)
