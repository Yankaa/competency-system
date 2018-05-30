from flask import render_template_string, jsonify, request
from services_info import append_comp_to_worker, remove_comp_from_worker, get_current_user, get_current_user_id


def render_table(view_competencies, added_competencies):
    print(view_competencies)
    print(added_competencies)
    return render_template_string(
        "{% import 'comp_table.html' as macro %}{{ macro.table(view_competencies, added_competencies) }}",
        view_competencies=view_competencies,
        added_competencies=added_competencies)


def change_competency_func():
    form = request.form
    request_type = form.get('type', 0, type=str)
    comp_id = form.get('comp_id', 0, type=int)
    user_id = get_current_user_id()
    if request_type == 'append':
        append_comp_to_worker(user_id, comp_id)
        return True
    elif request_type == 'remove':
        remove_comp_from_worker(user_id, comp_id)
        return False


def load_table(blueprint, path):
    def decorator(get_comps):
        @blueprint.route(path + '/change_competency', methods=['POST'])
        def change_competency(**kwargs):
            change_competency_func()
            return jsonify(table=render_table(get_comps(**kwargs), get_current_user()['competencies']))
        return change_competency
    return decorator
