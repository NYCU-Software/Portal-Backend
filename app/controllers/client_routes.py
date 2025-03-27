from flask import Blueprint, request, jsonify, current_app

client_bp = Blueprint("client_bp", __name__)

@client_bp.route("/exchange", methods=["POST"])
def exchange():
    data = request.json or {}
    code = data.get("code")
    client_id = data.get("client_id")
    client_secret = data.get("client_secret")
    redirect_uri = data.get("redirect_uri")
    if not code or not client_id or not client_secret or not redirect_uri:
        return jsonify({"error": "missing parameters"}), 400
    svc = current_app.hydra_service
    try:
        tokens = svc.exchange_code_for_token(code, redirect_uri, client_id, client_secret)
        return jsonify(tokens)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_bp.route("/userinfo", methods=["GET"])
def userinfo():
    token = request.args.get("access_token")
    if not token:
        return jsonify({"error": "missing access_token"}), 400
    svc = current_app.hydra_service
    try:
        info = svc.get_userinfo(token)
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
