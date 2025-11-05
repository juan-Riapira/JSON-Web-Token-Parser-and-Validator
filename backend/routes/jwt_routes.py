from flask import Blueprint, jsonify, request
from backend.services.jwt_services import analyze_token

routes_jwt = Blueprint('jwt', __name__)

@routes_jwt.route('/analyze-token', methods=['POST'])
def analyze_token_route():
    """
    Endpoint general que ejecuta los tres análisis:
    Léxico → Sintáctico → Semántico
    """
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"valid": False, "error": "No se recibió ningún token"}), 400

    result = analyze_token(token)
    return jsonify(result), (200 if result.get("valid") else 400)
