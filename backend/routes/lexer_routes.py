from flask import Blueprint, jsonify, request
from backend.lexer.lexer import lexical_analysis

routes_lexer = Blueprint('lexer', __name__)

@routes_lexer.route('/analyze-lexical', methods=['POST'])
def analyze_lexical():
    """
    Realiza solo el análisis LÉXICO del token.
    Verifica que tenga tres partes válidas separadas por puntos.
    """
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"valid": False, "error": "No se recibió ningún token"}), 400

    result = lexical_analysis(token)
    return jsonify(result), (200 if result["valid"] else 400)
