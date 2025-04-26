from functools import wraps
from flask import request, g, current_app

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = request.cookies.get("ory_kratos_session")
        #print(session_token)
        identity = None
        if session_token:
            identity = current_app.kratos_service.verify(session_token)
        g.user = identity.traits if identity else None
        return f(*args, **kwargs)
    return decorated_function