from functools import wraps

from flask import abort
from flask_login import current_user


def account_required(f):
    """Block partner users from accessing these routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.user_type != "account":
            abort(403)
        return f(*args, **kwargs)
    return decorated
