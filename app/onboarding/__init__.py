from flask import Blueprint

bp = Blueprint("onboarding", __name__, url_prefix="/onboarding")

from . import routes  # noqa: E402, F401
