from typing import Optional, NewType
from pydantic import BaseModel, EmailStr, validator, constr

TelefonoStr = NewType("TelefonoStr", str)
RFCStr = NewType("RFCStr", str)

class CuentaRegistro(BaseModel):
    nombre_empresa: str
    correo_contacto: EmailStr
    telefono_contacto: TelefonoStr
    pais: str
    responsable: Optional[str]
    rfc: Optional[RFCStr]
    direccion: Optional[str]

    @validator("telefono_contacto")
    def validar_telefono(cls, v):
        if not v.isdigit():
            raise ValueError("El teléfono debe contener solo números")
        if not (8 <= len(v) <= 15):
            raise ValueError("El teléfono debe tener entre 8 y 15 dígitos")
        return v

    @validator("rfc")
    def validar_rfc(cls, v):
        if v and not (12 <= len(v) <= 13):
            raise ValueError("El RFC debe tener entre 12 y 13 caracteres")
        return v