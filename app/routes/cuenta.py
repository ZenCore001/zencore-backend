# app/routes/cuenta.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.schemas.cuenta_schema import CuentaRegistro
from app.schemas.terminal_schema import TerminalCreate
from app.models.verificacion_pendiente import VerificacionPendiente
from app.models.cuenta_zensoftware import CuentaZenSoftware
from app.models.terminal import Terminal
from app.database.db import get_db
from app.utils.token_generator import generar_token_unico
from app.services.correo_service import enviar_correo_verificacion

router = APIRouter(prefix="/api/cuenta", tags=["Cuentas"])

# --------------------------
# REGISTRO INICIAL
# --------------------------
@router.post("/registro")
def registrar_cuenta(datos: CuentaRegistro, db: Session = Depends(get_db)):
    if db.query(VerificacionPendiente).filter_by(correo_contacto=datos.correo_contacto).first():
        raise HTTPException(status_code=400, detail="Ese correo ya está en proceso de verificación")

    if db.query(VerificacionPendiente).filter_by(telefono_contacto=datos.telefono_contacto).first():
        raise HTTPException(status_code=400, detail="Ese número de teléfono ya está en proceso de verificación")

    if datos.rfc:
        if db.query(VerificacionPendiente).filter_by(rfc=datos.rfc).first():
            raise HTTPException(status_code=400, detail="Ese RFC ya está en proceso de verificación")

    token = generar_token_unico()

    verificacion = VerificacionPendiente(
        nombre_empresa=datos.nombre_empresa,
        correo_contacto=datos.correo_contacto,
        telefono_contacto=datos.telefono_contacto,
        pais=datos.pais,
        responsable=datos.responsable,
        rfc=datos.rfc,
        direccion=datos.direccion,
        token_verificacion=token,
        fecha_solicitud=datetime.utcnow(),
        fecha_expiracion=datetime.utcnow() + timedelta(hours=1)
    )

    db.add(verificacion)
    db.commit()

    try:
        enviar_correo_verificacion(datos.correo_contacto, token)
    except Exception:
        db.delete(verificacion)
        db.commit()
        raise HTTPException(status_code=500, detail="Error al enviar el correo de verificación")

    return {"mensaje": "Por favor revisa tu bandeja de entrada y verifica tu correo"}


# --------------------------
# VERIFICACIÓN DE TOKEN
# --------------------------
@router.get("/verificar")
def verificar_token(token: str = Query(...), db: Session = Depends(get_db)):
    verificacion = db.query(VerificacionPendiente).filter_by(token_verificacion=token).first()

    if not verificacion:
        raise HTTPException(status_code=404, detail="Token inválido")

    if verificacion.fecha_expiracion < datetime.utcnow():
        db.delete(verificacion)
        db.commit()
        raise HTTPException(status_code=400, detail="El token ha expirado. Por favor inicia el registro de nuevo.")

    nueva_cuenta = CuentaZenSoftware(
        nombre_empresa=verificacion.nombre_empresa,
        correo_contacto=verificacion.correo_contacto,
        telefono_contacto=verificacion.telefono_contacto,
        pais=verificacion.pais,
        responsable=verificacion.responsable,
        rfc=verificacion.rfc,
        direccion=verificacion.direccion,
        correo_verificado=True,
        fecha_creacion=datetime.utcnow()
    )

    db.add(nueva_cuenta)
    db.delete(verificacion)
    db.commit()

    return {"mensaje": "Cuenta verificada con éxito. Ya puedes iniciar sesión en ZenCore."}


# --------------------------
# REENVIAR CORREO DE VERIFICACIÓN
# --------------------------
@router.post("/reenviar-verificacion")
def reenviar_correo_verificacion(correo: str = Query(...), db: Session = Depends(get_db)):
    cuenta = db.query(CuentaZenSoftware).filter_by(correo_contacto=correo).first()
    if cuenta and cuenta.correo_verificado:
        return {"mensaje": "Esta cuenta ya está verificada. Puedes iniciar sesión."}

    pendiente = db.query(VerificacionPendiente).filter_by(correo_contacto=correo).first()
    if not pendiente:
        raise HTTPException(status_code=404, detail="No hay verificación pendiente para este correo.")

    nuevo_token = generar_token_unico()
    pendiente.token_verificacion = nuevo_token
    pendiente.fecha_solicitud = datetime.utcnow()
    pendiente.fecha_expiracion = datetime.utcnow() + timedelta(hours=1)
    db.commit()

    try:
        enviar_correo_verificacion(correo, nuevo_token)
    except Exception:
        raise HTTPException(status_code=500, detail="Error al reenviar el correo de verificación")

    return {"mensaje": "Correo de verificación reenviado con éxito. Revisa tu bandeja de entrada."}


# --------------------------
# REGISTRAR TERMINAL
# --------------------------
@router.post("/registrar-terminal")
def registrar_terminal(datos: TerminalCreate, db: Session = Depends(get_db)):
    cuenta = db.query(CuentaZenSoftware).filter_by(correo_contacto=datos.correo_contacto, correo_verificado=True).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="No existe una cuenta verificada con ese correo.")

    if db.query(Terminal).filter_by(hardware_id=datos.hardware_id).first():
        raise HTTPException(status_code=400, detail="Esta terminal ya está registrada.")

    nueva_terminal = Terminal(
        hardware_id=datos.hardware_id,
        nombre=datos.nombre,
        cuenta_id=cuenta.id
    )

    db.add(nueva_terminal)
    db.commit()

    return {"mensaje": "Terminal registrada con éxito", "cuenta_id": cuenta.id}


# --------------------------
# PING
# --------------------------
@router.get("/ping")
def ping():
    return {"status": "ok"}