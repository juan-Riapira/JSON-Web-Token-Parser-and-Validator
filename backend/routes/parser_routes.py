from flask import Blueprint, jsonify, request
from backend.lexer.lexer import lexical_analysis
from backend.parser.parser import syntactic_analysis

routes_parser = Blueprint('parser', __name__)

@routes_parser.route('/analyze-syntactic', methods=['POST'])
def analyze_syntactic():
    """
    Realiza el análisis SINTÁCTICO del token JWT.
    Primero valida la estructura léxica, luego decodifica el JSON.
    """
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"valid": False, "error": "No se recibió ningún token"}), 400

    # 1️⃣ Análisis léxico primero
    lex_result = lexical_analysis(token)
    if not lex_result.get("valid"):
        return jsonify({
            "phase": "lexical",
            "valid": False,
            "error": lex_result.get("error")
        }), 400

    # 2️⃣ Análisis sintáctico
    syn_result = syntactic_analysis(lex_result["parts"])
    return jsonify(syn_result), (200 if syn_result["valid"] else 400)
