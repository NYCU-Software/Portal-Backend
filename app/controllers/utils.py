from functools import wraps
from flask import Flask, request, jsonify, abort, g, current_app


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get("Authorization")
        if authorization_header:
            token = authorization_header.replace("Bearer ", "", 1)
            try:
                g.token = token
                g.user = current_app.kratos_service.get_session_from_token(
                    token
                ).identity.traits
            except AttributeError:
                g.user = None
        else:
            g.user = None
        return f(*args, **kwargs)

    return decorated_function
