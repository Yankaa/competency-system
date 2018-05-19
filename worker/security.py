from flask_security import Security, SQLAlchemyUserDatastore, current_user, user_registered
from flask_security.forms import RegisterForm, StringField, Required
from database import db, User, Role
import services_info


class ExtendedRegisterForm(RegisterForm):
    full_name = StringField('Полное имя', [Required()])


def configure(app):
    with app.app_context():
        db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

    @user_registered.connect_via(app)
    def user_registered_(__, user, **_):
        worker_id = services_info.add_worker(user.full_name)
        user.worker_id = worker_id
        db.session.commit()


def get_current_user_id() -> int:
    return current_user.worker_id
