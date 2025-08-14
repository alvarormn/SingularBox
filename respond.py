def parse_booking_response(resp: dict) -> dict:
    """
    Devuelve un dict con:
      - status: "ok" | "error"
      - code:   código interno normalizado
      - state:  bookState original
      - detail: mensaje en claro (cuando aplica)
    """
    if not resp:
        return {"status": "error", "code": "NO_RESPONSE", "state": None,
                "detail": "No se recibió respuesta del servidor."}

    state = resp.get("bookState")

    # Éxito (el propio front trata 1 y 0 como OK)
    if state in (0, 1):
        return {"status": "ok", "code": "BOOKED", "state": state,
                "detail": "Reserva realizada correctamente."}

    # Límite de reservas en la misma clase por día
    if state == -8:
        return {"status": "error", "code": "LIMIT_SAME_CLASS_PER_DAY", "state": state,
                "detail": "Ya tienes reservas ese día para esa clase."}

    # No permitido todavía (mirar la causa concreta)
    if state == -12:
        lang = resp.get("errorMssgLang")  # viene del backend
        if lang == "ERROR_ANTELACION_CLIENTE_HORAS":
            return {"status": "error", "code": "TOO_SOON_HOURS", "state": state,
                    "detail": "Solo se puede reservar con 3 horas de antelación."}
        if lang == "ERROR_ANTELACION_CLIENTE":
            return {"status": "error", "code": "TOO_SOON_DAYS", "state": state,
                    "detail": "Solo se puede reservar con 3 días de antelación."}
        # fallback genérico con el mensaje crudo si existe
        return {"status": "error", "code": "NOT_ALLOWED", "state": state,
                "detail": resp.get("errorMssg", "No puedes acceder a esa clase.")}

    # Otros estados que el front maneja (por si quieres completarlos)
    if state == -1:
        return {"status": "error", "code": "CLASS_FULL", "state": state,
                "detail": "La clase está llena."}
    if state == -4:
        return {"status": "error", "code": "TOO_EARLY_GLOBAL_LIMIT", "state": state,
                "detail": "No puedes reservar con más de 3 días de antelación."}
    if state == -5:
        return {"status": "error", "code": "PENDING_PAYMENT", "state": state,
                "detail": "Pago pendiente; no se pudo hacer la reserva."}
    if state == -7:
        # En el front lo formatean con horas/minutos; aquí dejamos genérico
        return {"status": "error", "code": "TOO_LATE_BEFORE_CLASS", "state": state,
                "detail": "No puedes reservar con tan poca antelación."}

    # Desconocido
    return {"status": "error", "code": f"UNKNOWN_{state}", "state": state,
            "detail": "Estado de reserva no reconocido."}
