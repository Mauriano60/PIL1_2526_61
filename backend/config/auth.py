from functools import wraps
from flask import session
from utils.responses import error_response

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if "user_id" not in session:
            return error_response(
                "Authentification requise",
                401
            )

        return f(*args, **kwargs)

    return decorated