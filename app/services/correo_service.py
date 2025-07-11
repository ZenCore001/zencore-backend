# services/correo_service.py
def enviar_correo_verificacion(correo: str, token: str):
    enlace = f"https://zensoftware.mx/verificar?token={token}"
    asunto = "Verifica tu correo - ZenCore"
    cuerpo = f"""
    Hola! Gracias por registrarte en ZenCore.
    Para continuar, haz clic en el siguiente enlace:

    {enlace}

    Este enlace expirará en 1 hora.
    """
    # Aquí conectas tu sistema real de envío (SMTP, SendGrid, etc)
    print(f"Enviando correo a {correo} con enlace: {enlace}")