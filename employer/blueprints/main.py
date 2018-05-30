from flask import Blueprint, render_template, redirect, url_for
from services_info import get_current_user, get_current_user_id, get_employer_works
from flask_security import login_required, logout_user

main_page = Blueprint('main_page', __name__, template_folder='templates')


@main_page.route('/')
@login_required
def index():
    return render_template("index.html", user=get_current_user(), works=get_employer_works(get_current_user_id()))


@main_page.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))
