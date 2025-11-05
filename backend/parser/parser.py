import base64
import json

def base64url_decode(data: str) -> str:
    """
    Decodifica una cadena Base64URL a texto UTF-8.
    """
    padding = '=' * (4 - len(data) % 4)
    try:
        return base64.urlsafe_b64decode(data + padding).decode('utf-8')
    except Exception:
        raise ValueError("Base64 inválido")

def syntactic_analysis(parts: list[str]):
    """
    Recibe las 3 partes (ya validadas por el lexer):
    header, payload, signature.
    Verifica que las dos primeras partes sean JSON válidos.
    """
    if len(parts) != 3:
        return {
            "phase": "syntactic",
            "valid": False,
            "error": "No se recibieron las tres partes del token"
        }

    try:
        header_decoded = base64url_decode(parts[0])
        payload_decoded = base64url_decode(parts[1])
        header = json.loads(header_decoded)
        payload = json.loads(payload_decoded)
        signature = parts[2]

        return {
            "phase": "syntactic",
            "valid": True,
            "message": "Estructura JSON válida",
            "header": header,
            "payload": payload,
            "signature": signature
        }

    except json.JSONDecodeError:
        return {
            "phase": "syntactic",
            "valid": False,
            "error": "Error al decodificar: JSON mal formado"
        }

    except ValueError:
        return {
            "phase": "syntactic",
            "valid": False,
            "error": "Error al decodificar: Base64 inválido"
        }
