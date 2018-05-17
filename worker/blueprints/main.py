from flask import Blueprint, render_template
from services_info import get_current_user, get_professions, get_areas

main_page = Blueprint('main_page', __name__, template_folder='templates')


@main_page.route('/')
def index():
    return render_template("index.html", user=get_current_user(), professions=get_professions(), areas=get_areas())
