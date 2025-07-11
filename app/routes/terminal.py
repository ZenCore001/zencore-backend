# routes/terminal.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.db import get_db
from app.models.terminal import Terminal
from app.models.cuenta_zensoftware import CuentaZenSoftware
from app.schemas.terminal_schema import TerminalRegistro
from app.models.terminal import Terminal
from app.schemas.terminal_schema import TerminalCreate

router = APIRouter(prefix="/api/terminal", tags=["Terminales"])

@router.post("/registrar")
def registrar_terminal(datos: TerminalRegistro, db: Session = Depends(get_db)):
    # Verificar si la terminal ya está registrada
    if db.query(Terminal).filter_by(hardware_id=datos.hardware_id).first():
        raise HTTPException(status_code=400, detail="Este hardware ya está registrado como terminal")

    # Verificar que la cuenta exista
    cuenta = db.query(CuentaZenSoftware).filter_by(id=datos.cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta de empresa no encontrada")

    # Contar cuántas terminales tiene esta cuenta (para numerar)
    total_terminales = db.query(Terminal).filter_by(cuenta_id=datos.cuenta_id).count()
    numero_terminal = total_terminales + 1

    # Generar nombre si no se envió
    nombre_logico = datos.nombre or f"ZEN-{datos.cuenta_id}-T{numero_terminal}"

    # Crear y guardar la nueva terminal
    terminal = Terminal(
        hardware_id=datos.hardware_id,
        cuenta_id=datos.cuenta_id,
        nombre=nombre_logico,
        fecha_registro=datetime.utcnow()
    )

    db.add(terminal)
    db.commit()
    db.refresh(terminal)

    return {
        "mensaje": "Terminal registrada con éxito",
        "nombre": terminal.nombre,
        "terminal_id": terminal.id,
        "cuenta_id": terminal.cuenta_id
    }
    

@router.post("/registrar-terminal")
def registrar_terminal(datos: TerminalCreate, db: Session = Depends(get_db)):
    # Verificar que la cuenta exista y esté verificada
    cuenta = db.query(CuentaZenSoftware).filter_by(correo_contacto=datos.correo_contacto, correo_verificado=True).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="No existe una cuenta verificada con ese correo.")

    # Validar si ya existe el hardware_id
    if db.query(Terminal).filter_by(hardware_id=datos.hardware_id).first():
        raise HTTPException(status_code=400, detail="Esta terminal ya está registrada.")

    # Crear la terminal
    nueva_terminal = Terminal(
        hardware_id=datos.hardware_id,
        nombre=datos.nombre,
        cuenta_id=cuenta.id
    )
    db.add(nueva_terminal)
    db.commit()

    return {"mensaje": "Terminal registrada con éxito", "cuenta_id": cuenta.id}