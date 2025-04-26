from flask import Blueprint, g, jsonify
from .utils import authenticate

user_bp = Blueprint('user', __name__)

@user_bp.route('/whoami', methods=['GET'])
@authenticate
def whoami():
    if g.user:
        return jsonify(g.user), 200
    return jsonify({'error': 'unauthorized'}), 401
