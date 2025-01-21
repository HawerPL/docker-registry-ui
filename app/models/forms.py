from flask import current_app
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import Length, DataRequired
from flask_wtf import FlaskForm
from flask_babel import _


class LoginForm(FlaskForm):
    username = StringField(label=_("Username"), render_kw={"placeholder": _("Username")}, validators=[DataRequired(), Length(1, 32)])
    password = PasswordField(label=_("Password"), render_kw={"placeholder": _("Password")}, validators=[DataRequired(), Length(1, 32)])
    registry = SelectField(label=_("Registry"), coerce=str, validators=[DataRequired()])
    loginSubmit = SubmitField(_("Sign in"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.populate_registry_choices()

    def populate_registry_choices(self):
        self.registry.choices = [(reg.url, f"{reg.name} ({reg.url})") for reg in current_app.config.get('REGISTRIES', [])]

        if current_app.config.get('SUPER_USER_ENABLED', False):
            self.registry.choices.append((current_app.config.get('SPECIAL_REGISTRY_KEY', ''), _("All registries")))

    def validate(self):
        initial_validation = super().validate()
        if not initial_validation:
            return False

        return True