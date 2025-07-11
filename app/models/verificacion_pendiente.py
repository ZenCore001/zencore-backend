from sqlalchemy import Column, Integer, String, DateTime
from app.database.db import Base
from datetime import datetime, timedelta

class VerificacionPendiente(Base):
    __tablename__ = "verificaciones_pendientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String, nullable=False)
    correo_contacto = Column(String, nullable=False)
    telefono_contacto = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    responsable = Column(String, nullable=True)
    rfc = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    token_verificacion = Column(String, nullable=False, unique=True)
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    fecha_expiracion = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=1))