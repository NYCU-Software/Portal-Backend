import json
from flask import Blueprint, request, jsonify, current_app, abort, g
from .utils import authenticate

authorization_bp = Blueprint("authenrization", __name__)


@authorization_bp.route("/consent", methods=["GET"])
@authenticate
def get_consent():
    data = request.args or {}
    challenge = data.get("consent_challenge")
    if not challenge:
        return jsonify({"error": "missing consent_challenge"}), 400
    hydra_svc = current_app.hydra_service
    try:
        info = hydra_svc.get_consent_request(challenge)
        return jsonify(
            {
                "client_name": info.get("client", {}).get("client_name"),
                "requested_scopes": info.get("requested_scope", []),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@authorization_bp.route("/consent/accept", methods=["POST"])
@authenticate
def accept_consent():
    data = request.get_json() or {}
    challenge = data.get("consent_challenge")
    if not challenge:
        return jsonify({"error": "missing consent_challenge"}), 400
    if not g.user:
        abort(401)
    hydra_svc = current_app.hydra_service
    try:
        url = hydra_svc.accept_consent_request(
            consent_challenge=challenge,
            user_info={
                "grant_scope": ["openid", "offline"],
                "grant_access_token_audience": [],
                "remember": True,
                "remember_for": 3600,
                "session": {
                    "id_token": {
                        "custom_claim": "value",
                        "email": g.user["email"],
                        "username": g.user["username"],
                    }
                },
            },
        )
        return jsonify({"url": url})
    except Exception as e:
        raise (e)
        return jsonify({"error": str(e)}), 500


@authorization_bp.route("/consent/reject", methods=["POST"])
def reject_consent():
    data = request.get_json() or {}
    challenge = data.get("consent_challenge")
    if not g.user:
        abort(401)
    if not challenge:
        return jsonify({"error": "missing consent_challenge"}), 400
    reason = data.get("reason", "User rejected the consent")
    hydra_svc = current_app.hydra_service
    try:
        url = hydra_svc.reject_consent_request(challenge, reason)
        return jsonify({"url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
