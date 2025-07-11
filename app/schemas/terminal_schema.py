# schemas/terminal_schema.py
from pydantic import BaseModel

class TerminalCreate(BaseModel):
    hardware_id: str
    nombre: str
    correo_contacto: str  # Para buscar la cuenta a la que se va a asociar