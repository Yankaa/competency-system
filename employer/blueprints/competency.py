from flask import Blueprint, jsonify, render_template, request
from services_info import get_current_user, get_competency, get_work_info
from .competency_table import change_competency_func
from flask_security import login_required

competency_page = Blueprint('competency_page', __name__, template_folder='templates')


@competency_page.route('/competency/<int:comp_id>')
@login_required
def competency(comp_id: int):
    work_id = request.args.get('work', 0, type=int)
    work = get_work_info(work_id, load_comps=False) if work_id else None
    return render_template("competency.html", user=get_current_user(), competency=get_competency(comp_id), work=work)


@competency_page.route('/change_competency_1', methods=['POST'])
@login_required
def change_competency_1():
    return jsonify(is_added=change_competency_func())
