from flask import Blueprint, render_template, jsonify, request, render_template_string
from services_info import get_current_user, get_professions, get_competencies, get_areas, get_area_profs
from blueprints.competency_table import render_table, change_competency_func
from flask_security import login_required

manage_competencies_page = Blueprint('manage_competencies_page', __name__, template_folder='templates')


@manage_competencies_page.route('/manage_competencies')
@login_required
def manage_competencies():
    return render_template("manage_competencies.html", user=get_current_user(), professions=get_professions(), areas=get_areas())


@manage_competencies_page.route('/change_competency', methods=['POST'])
@login_required
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


_option_template = "{% import 'profession_select.html' as macro %}{{ macro.profession_select(professions, disabled) }}"


@manage_competencies_page.route('/get_prof_comps', methods=['POST'])
@login_required
def get_prof_comps():
    form = request.form
    area_id = form.get('area_id', 0, type=int)
    prof_id = form.get('prof_id', 0, type=int)
    description = form.get('description', None, type=str)
    update_prof = form.get('update_prof', False, type=bool)

    user_comps = get_current_user()['competencies']
    found_comp_table = render_table(get_competencies(area_id, prof_id, description), user_comps)

    if update_prof:
        return jsonify(
            found_comp_table=found_comp_table,
            prof_select=render_template_string(_option_template, professions=get_area_profs(area_id), disabled=area_id == 0)
        )
    else:
        return jsonify(found_comp_table=found_comp_table)
