from flask_security import Security, SQLAlchemyUserDatastore, current_user, user_registered
from flask_security.forms import RegisterForm, StringField, Required
from wtforms.fields.simple import TextAreaField
from database import db, User, Role
import services_info


class ExtendedRegisterForm(RegisterForm):
    employer_name = StringField('Наименование работодателя', [Required()])
    employer_description = TextAreaField('Описание работодателя', [Required()])


def configure(app):
    with app.app_context():
        db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

    @user_registered.connect_via(app)
    def user_registered_(__, user, **_):
        employer_id = services_info.add_employer(user.employer_name, user.employer_description)
        user.employer_id = employer_id
        db.session.commit()


def get_current_user_id() -> int:
    return current_user.employer_id
