from flask import Blueprint, render_template, jsonify, request
from services_info import get_current_user, get_professions, get_competencies, get_areas
from blueprints.competency_table import render_table, change_competency_func

manage_competencies_page = Blueprint('manage_competencies_page', __name__, template_folder='templates')


@manage_competencies_page.route('/manage_competencies')
def manage_competencies():
    return render_template("manage_competencies.html", user=get_current_user(), professions=get_professions(), areas=get_areas())


@manage_competencies_page.route('/change_competency', methods=['POST'])
def change_competency():
    change_competency_func()
    form = request.form
    prof_id = form.get('prof_id', 0, type=int)
    area_id = form.get('area_id', 0, type=int)
    found_comps = get_competencies(area_id, prof_id)
    user_comps = get_current_user()['competencies']
    return jsonify(
        found_comp_table=render_table(found_comps, user_comps),
        user_comp_table=render_table(user_comps, None)
    )


@manage_competencies_page.route('/get_prof_comps', methods=['POST'])
def get_prof_comps():
    form = request.form
    prof_id = form.get('prof_id', 0, type=int)
    area_id = form.get('area_id', 0, type=int)
    user_comps = get_current_user()['competencies']
    return jsonify(found_comp_table=render_table(get_competencies(area_id, prof_id), user_comps))
