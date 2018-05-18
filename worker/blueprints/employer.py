from flask import Blueprint, render_template
from services_info import get_employer_info, get_current_user, get_employer_works
from flask_security import login_required

employer_page = Blueprint('employer_page', __name__, template_folder='templates')


@employer_page.route('/employer/<int:employer_id>')
@login_required
def employer(employer_id: int):
    return render_template("employer.html",
                           user=get_current_user(),
                           employer=get_employer_info(employer_id),
                           works=get_employer_works(employer_id))
