from flask import Blueprint, jsonify, render_template, request
from services_info import get_current_user, get_current_user_id, append_comp_to_worker, remove_comp_from_worker, get_competency
from flask_security import login_required

competency_page = Blueprint('competency_page', __name__, template_folder='templates')


@competency_page.route('/competency/<int:comp_id>')
@login_required
def competency(comp_id: int):
    return render_template("competency.html", user=get_current_user(), competency=get_competency(comp_id))


@competency_page.route('/change_competency_1', methods=['POST'])
@login_required
def change_competency_1():
    form = request.form
    request_type = form.get('type', 0, type=str)
    comp_id = form.get('comp_id', 0, type=int)
    user_id = get_current_user_id()
    if request_type == 'append':
        append_comp_to_worker(user_id, comp_id)
        return jsonify(is_added=True)
    elif request_type == 'remove':
        remove_comp_from_worker(user_id, comp_id)
        return jsonify(is_added=False)
