from flask import Blueprint, request, jsonify, current_app, abort, g
from .utils import authenticate

user_bp = Blueprint("user", __name__)

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    identifier = data.get("identifier")
    password = data.get("password")
    login_challenge = data.get("login_challenge")

    if not identifier or not password:
        return jsonify({"error": "Missing identifier or password"}), 400

    session_token = current_app.kratos_service.login(identifier, password)

    if not session_token:
        return jsonify({"error": "Invalid credentials"}), 401

    if login_challenge:
        session_info = current_app.kratos_service.get_session_from_token(session_token)
        
        if not session_info:
            return jsonify({"error": "Session retrieval failed"}), 401

        user = session_info.identity.traits
        user = {
            'subject': session_info.identity.id
        }
        url = current_app.hydra_service.accept_login_request(login_challenge, user)
        return jsonify({"token": session_token, "url": url})

    return jsonify({"token": session_token, "url": "/"})


@user_bp.route("/whoami")
@authenticate
def whoami():
    if g.user:
        return g.user
    abort(401)

@user_bp.route("/logout")
@authenticate
def logout():
    if g.user:
        current_app.kratos_service.logout(g.token)
        return {"msg": "ok"}
    abort(401)

@user_bp.route("/authorize", methods=["POST"])
@authenticate
def authorize():
    data = request.get_json() or {}
    login_challenge = data.get("login_challenge")
    if not login_challenge:
        return jsonify({"error": "missing login_challenge"}), 400

    session_info = current_app.kratos_service.get_session_from_token(g.token)
    if not session_info:
        return jsonify({"error": "Session retrieval failed"}), 401

    identity = session_info.identity
    user = {
        "subject": identity.id,
    }
    url = current_app.hydra_service.accept_login_request(login_challenge, user)
    return jsonify({"token": g.token, "url": url})

