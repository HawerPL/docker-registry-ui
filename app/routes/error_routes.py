from flask import Blueprint, render_template
from flask_babel import _


bp = Blueprint('error', __name__)


@bp.errorhandler(400)
def bad_request(error):
    return render_template("error.html", error_code="400")


@bp.errorhandler(403)
def forbidden(error):
    return render_template("error.html", error_code="403")


@bp.errorhandler(404)
def not_found(error):
    return render_template("error.html", error_code="404")


@bp.errorhandler(500)
def server_error(error):
    return render_template("error.html", error_code="500")
