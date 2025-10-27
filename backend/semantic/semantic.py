from datetime import datetime, timezone

def semantic_analysis(header: dict, payload: dict):
    """
    Realiza el análisis SEMÁNTICO de un token JWT.
    -----------------------------------------------
    En esta etapa ya se supone que:
      - El análisis léxico fue exitoso (el token tiene 3 partes válidas)
      - El análisis sintáctico fue exitoso (header y payload son JSON válidos)

    Objetivo:
      Analizar el significado lógico del contenido del token.
      Es decir, verificar que los campos que definen su validez temporal
      y su algoritmo de firma tengan sentido.

    Validaciones que realiza:
      1Algoritmo (alg) soportado: "HS256" o "HS384"
      2 Campo de expiración (exp): que no esté vencido
      3Campo de validez futura (nbf): que el token no sea válido antes de tiempo
      4Campo de emisión (iat): que tenga formato correcto
      5 Coherencia general de los tiempos
    """

    errors = []  # Lista para registrar los errores encontrados
    now = datetime.now(timezone.utc).timestamp()  # Tiempo actual (UTC)
    algorithm = header.get("alg")

    # Verificar algoritmo soportado
    if algorithm not in ["HS256", "HS384"]:
        errors.append(f"Algoritmo no soportado: {algorithm}")

    # Verificar expiración (exp)
    exp = payload.get("exp")
    if exp is not None:
        if not isinstance(exp, (int, float)):
            errors.append("El campo 'exp' debe ser numérico (timestamp).")
        elif now > exp:
            errors.append("El token ha expirado (exp).")

    # Verificar "not before" (nbf)
    nbf = payload.get("nbf")
    if nbf is not None:
        if not isinstance(nbf, (int, float)):
            errors.append("El campo 'nbf' debe ser numérico (timestamp).")
        elif now < nbf:
            errors.append("El token aún no es válido (nbf en el futuro).")

    # Verificar "issued at" (iat)
    iat = payload.get("iat")
    if iat is not None:
        if not isinstance(iat, (int, float)):
            errors.append("El campo 'iat' debe ser numérico (timestamp).")
        elif iat > now:
            errors.append("El campo 'iat' indica una fecha futura (no válido).")

    # Resultado final del análisis
    valid = len(errors) == 0

    return {
        "phase": "semantic",
        "valid": valid,
        "algorithm": algorithm,
        "errors": errors,
        "message": "Token válido semánticamente" if valid else "Se detectaron errores semánticos",
        "checked_fields": {
            "alg": algorithm,
            "exp": exp,
            "nbf": nbf,
            "iat": iat
        },
        "timestamp_analysis": datetime.now(timezone.utc).isoformat()
    }
