from flask import Blueprint, jsonify, request
from datetime import datetime
from backend.lexer.lexer import lexical_analysis
from backend.parser.parser import syntactic_analysis
from backend.semantic.semantic import semantic_analysis
from backend.db.connection import get_collection

routes_semantic = Blueprint('semantic', __name__)

@routes_semantic.route('/analyze-semantic', methods=['POST'])
def analyze_semantic():
    """
    Realiza el análisis SEMÁNTICO del token JWT.
    - Verifica estructura léxica.
    - Decodifica contenido JSON.
    - Analiza validez temporal y algoritmo.
    - Guarda el token en MongoDB (solo el texto del token).
    """
    data = request.get_json()
    token = data.get("token")
    collection = get_collection()

    if not token:
        return jsonify({"valid": False, "error": "No se recibió ningún token"}), 400

    # 1️⃣ Léxico
    lex_result = lexical_analysis(token)
    if not lex_result.get("valid"):
        return jsonify(lex_result), 400

    # 2️⃣ Sintáctico
    syn_result = syntactic_analysis(lex_result["parts"])
    if not syn_result.get("valid"):
        return jsonify(syn_result), 400

    # 3️⃣ Semántico
    sem_result = semantic_analysis(syn_result["header"], syn_result["payload"])

    # ✅ Guardar el token en MongoDB
    collection.insert_one({
        "token": token,
        "fecha_guardado": datetime.utcnow()
    })

    return jsonify(sem_result), (200 if sem_result["valid"] else 400)
