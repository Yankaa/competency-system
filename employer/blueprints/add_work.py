from flask import Blueprint, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_security import login_required
from services_info import get_current_user, get_current_user_id, add_work as add_work_

add_work_page = Blueprint('add_work_page', __name__, template_folder='templates')


class AddWorkForm(FlaskForm):
    description = StringField('Название вакансии', validators=[DataRequired()])
    salary = IntegerField('Зарплата', validators=[NumberRange(min=1)])
    submit = SubmitField('Создать вакансию')


@add_work_page.route('/add_work', methods=('GET', 'POST'))
@login_required
def add_work():
    form = AddWorkForm()
    if form.validate_on_submit():
        work_id = add_work_(get_current_user_id(), form.description.data, form.salary.data)
        return redirect('/work/%d' % work_id)
    return render_template('add_work.html', user=get_current_user(), form=form)
