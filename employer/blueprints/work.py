from flask import Blueprint, render_template
from services_info import get_work_info, get_current_user
from flask_security import login_required

work_page = Blueprint('work_page', __name__, template_folder='templates')


@work_page.route('/work/<int:work_id>')
@login_required
def work(work_id: int):
    return render_template("work.html", user=get_current_user(), work=get_work_info(work_id))
