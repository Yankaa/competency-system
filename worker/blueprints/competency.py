from flask import Blueprint, jsonify, render_template
from services_info import get_current_user, get_competency
from flask_security import login_required
from .competency_table import change_competency_func

competency_page = Blueprint('competency_page', __name__, template_folder='templates')


@competency_page.route('/competency/<int:comp_id>')
@login_required
def competency(comp_id: int):
    return render_template("competency.html", user=get_current_user(), competency=get_competency(comp_id))


@competency_page.route('/change_competency_1', methods=['POST'])
@login_required
def change_competency_1():
    return jsonify(is_added=change_competency_func())
