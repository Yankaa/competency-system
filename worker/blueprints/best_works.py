from flask import Blueprint, render_template
from services_info import get_current_user, get_best_works
from flask_security import login_required

best_works_page = Blueprint('best_works_page', __name__, template_folder='templates')


@best_works_page.route('/best_works')
@login_required
def best_works():
    user = get_current_user()
    return render_template("best_works.html", user=user, best_works=get_best_works(user['id']))
