from flask import Blueprint, request, jsonify, current_app
from jsonschema import validate, ValidationError

CLIENT_SCHEMA = {
    "type": "object",
    "properties": {
        "client_id": {"type": "string"},
        "response_types": {"type": "array", "items": {"type": "string"}},
        "redirect_uris": {
            "type": "array",
            "items": {"type": "string", "format": "uri"},
        },
        "client_secret": {"type": "string"},
    },
    "required": [
        "client_id",
        "client_name",
        "redirect_uris",
        "client_secret",
    ],
}

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
        tokens = svc.exchange_code_for_token(
            code, redirect_uri, client_id, client_secret
        )
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


@client_bp.route("/clients", methods=["POST"])
def create_client_route():
    data = request.get_json()
    data['grant_type'] = 'authorization_code'
    data['response_type'] = 'code'
    try:
        validate(instance=data, schema=CLIENT_SCHEMA)
    except ValidationError as e:
        return jsonify({"error": "Invalid format", "details": e.message}), 400

    try:
        result = current_app.hydra_service.create_client(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(result), 201


@client_bp.route("/clients/<client_id>", methods=["PUT"])
def update_client_route(client_id):
    data = request.get_json()
    data['grant_type'] = 'authorization_code'
    data['response_type'] = 'code'
    try:
        validate(instance=data, schema=CLIENT_SCHEMA)
    except ValidationError as e:
        return jsonify({"error": "Invalid format", "details": e.message}), 400

    try:
        result = current_app.hydra_service.update_client(client_id, data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(result)


@client_bp.route("/clients/<client_id>", methods=["GET"])
def get_client_route(client_id):
    try:
        result = current_app.hydra_service.get_client(client_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(result)


@client_bp.route("/clients/<client_id>", methods=["DELETE"])
def delete_client_route(client_id):
    try:
        result = current_app.hydra_service.delete_client(client_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(result)


@client_bp.route("/clients/", methods=["GET"])
def get_all_clients_route():
    try:
        result = current_app.hydra_service.get_clients()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(result)
