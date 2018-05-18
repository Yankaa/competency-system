from flask import Blueprint, render_template
from services_info import get_current_user, get_current_user_id, get_demanded_competencies, get_competency
from blueprints.competency_table import load_table
from flask_security import login_required

demanded_competencies_page = Blueprint('demanded_competencies_page', __name__, template_folder='templates')


def get_demanded_comps():
    return [get_competency(comp_id) for comp_id in get_demanded_competencies(get_current_user_id())]


@demanded_competencies_page.route('/demanded_competencies')
@login_required
def demanded_competencies():
    return render_template("demanded_competencies.html", user=get_current_user(), demanded_competencies=get_demanded_comps())


@load_table(demanded_competencies_page, '/demanded_competencies')
@login_required
def change_competency():
    return get_demanded_comps()
