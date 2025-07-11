# models/cuenta_zensoftware.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base

class CuentaZenSoftware(Base):
    __tablename__ = "cuentas_zensoftware"

    id = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String, nullable=False)
    correo_contacto = Column(String, unique=True, nullable=False)
    telefono_contacto = Column(String, unique=True, nullable=False)
    pais = Column(String, nullable=False)
    responsable = Column(String, nullable=True)
    rfc = Column(String, unique=True, nullable=True)
    direccion = Column(String, nullable=True)
    correo_verificado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # 🔁 Relación con terminales
    terminales = relationship("Terminal", back_populates="cuenta")