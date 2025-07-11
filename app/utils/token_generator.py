import uuid

def generar_token_unico() -> str:
    return str(uuid.uuid4())