import flask_login
from flask import Blueprint, render_template, url_for, redirect, request, session, current_app
from flask_login import logout_user, login_required
from flask_babel import _

from app.config import update_special_registry_key
from app.models.forms import LoginForm
from app.models.user import is_authorized, users, is_superuser
from app.services.registry_service import update_registry_access

bp = Blueprint('app', __name__)


@bp.route("/")
@login_required
def main():

    if not current_app.config['ENABLED_AUTH']:
        registry_url = current_app.config['SPECIAL_REGISTRY_KEY']
        session['registry_url'] = registry_url
        session['is_super_user'] = True
        session['username'] = "Superuser"

    return render_template("base.html", name="index")


@bp.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registry_url = request.form['registry']

        update_registry_access()

        if username is not None and password is not None and registry_url is not None:
            if (registry_url == current_app.config['SPECIAL_REGISTRY_KEY'] and
                    is_superuser(username, password, current_app.config['SUPER_USER_LOGIN'],
                                 current_app.config['SUPER_USER_PASSWORD'])):
                user = next((user for user in users if
                             user.username == username and user.password == password), None)
                flask_login.login_user(user)
                session['registry_url'] = registry_url
                session['is_super_user'] = True
                session['username'] = username
                update_special_registry_key()
                return redirect(url_for('app.main'))
            else:
                authentication_registry_result = is_authorized(username, password, registry_url)
                if authentication_registry_result == 200:

                    registry = next((registry for registry in current_app.config['REGISTRIES'] if
                                     registry_url == registry.url), None)
                    user = next((user for user in users if
                                 user.username == username and user.password == password and
                                 user.registry.url == registry.url), None)
                    flask_login.login_user(user)
                    session['registry_url'] = registry_url
                    session['username'] = username
                    return redirect(url_for('app.main'))
                else:
                    return render_template("login.html", name="login", login_form=LoginForm(),
                                           app_name=current_app.config['APP_NAME'], enabled_logo=current_app.config['ENABLED_LOGO'], error_msg="")
                    # Może implementacja notyfikacji

    if current_app.config['ENABLED_AUTH']:
        return render_template("login.html", name="login", login_form=LoginForm(),
                               app_name=current_app.config['APP_NAME'], enabled_logo=current_app.config['ENABLED_LOGO'])
    else:
        return redirect(url_for('app.main'))


@bp.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("app.login"))


@bp.context_processor
def inject_custom_variables():
    return dict(app_name=current_app.config['APP_NAME'])


@bp.route("/change-language/<language_code>", methods=["GET", ""])
def change_language(language_code):
    session['language'] = language_code
    return redirect(request.referrer)


@bp.route("/change-theme/<theme>", methods=["GET", ""])
def change_theme(theme):
    session['theme'] = theme
    return redirect(request.referrer)

