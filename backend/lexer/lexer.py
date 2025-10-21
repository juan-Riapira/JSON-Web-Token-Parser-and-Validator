import re

def lexical_analysis(token: str):
    pattern = re.compile(r'^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$')
    if not pattern.match(token):
        return {"valid": False, "error": "Formato inválido (JWT debe tener 3 partes válidas)"}
    parts = token.split('.')
    return {"valid": True, "parts": parts}