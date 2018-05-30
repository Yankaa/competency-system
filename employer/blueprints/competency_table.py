from flask import render_template_string, jsonify, request
from services_info import append_comp_to_work, remove_comp_from_work, get_work_info


def get_current_work(from_args: bool = False):
    if from_args:
        work_id = request.args.get('work', 0, type=int)
        if not work_id:
            return None
    else:
        work_id = request.form.get('work_id', 0, type=int)
    return get_work_info(work_id)


def render_table(view_competencies, work):
    if view_competencies is None:
        view_competencies = work['competencies']
        added_competencies = None
    else:
        added_competencies = work['competencies']
    return render_template_string(
        "{% import 'comp_table.html' as macro %}{{ macro.table(view_competencies, added_competencies, work_id=work_id) }}",
        view_competencies=view_competencies,
        added_competencies=added_competencies,
        work_id=work['id'])


def change_competency_func():
    form = request.form
    request_type = form.get('type', 0, type=str)
    comp_id = form.get('comp_id', 0, type=int)
    work_id = form.get('work_id', 0, type=int)

    if request_type == 'append':
        append_comp_to_work(work_id, comp_id)
        return True
    elif request_type == 'remove':
        remove_comp_from_work(work_id, comp_id)
        return False


def load_table(blueprint, path):
    def decorator(get_comps):
        @blueprint.route(path + '/change_competency', methods=['POST'])
        def change_competency(**kwargs):
            change_competency_func()
            return jsonify(table=render_table(get_comps(**kwargs), get_current_work()))
        return change_competency
    return decorator
