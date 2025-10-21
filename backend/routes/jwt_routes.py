from flask import  jsonify, request , Blueprint
from backend.lexer.lexer import lexical_analysis

routes = Blueprint('inventario', __name__)
# Ruta para analizar el token
@routes.route('/analyze', methods=['POST'])
def analyze_token():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"valid": False, "error": "No se recibió ningún token"}), 400

    result = lexical_analysis(token)
    return jsonify(result), 200