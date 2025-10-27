# backend/services/jwt_services.py
from backend.lexer.lexer import lexical_analysis
from backend.parser.parser import syntactic_analysis
from backend.semantic.semantic import semantic_analysis
from backend.db.connection import get_collection
from datetime import datetime

def analyze_token(token: str):
    """
    Ejecuta los tres análisis y guarda el token en MongoDB.
    Devuelve solo el resultado semántico.
    """
    #  Léxico
    lex = lexical_analysis(token)
    if not lex["valid"]:
        return {"phase": "lexical", "valid": False, "error": lex["error"]}

    # Sintáctico
    syn = syntactic_analysis(lex["parts"])
    if not syn["valid"]:
        return {"phase": "syntactic", "valid": False, "error": syn["error"]}

    # semántico
    sem = semantic_analysis(syn["header"], syn["payload"])

    # Guardar solo el token
    collection = get_collection()
    collection.insert_one({
        "token": token,
        "fecha_guardado": datetime.utcnow()
    })

    return {"phase": "semantic", **sem}
