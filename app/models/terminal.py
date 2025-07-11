from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base

class Terminal(Base):
    __tablename__ = "terminales"

    id = Column(Integer, primary_key=True, index=True)
    hardware_id = Column(String, unique=True, nullable=False)
    cuenta_id = Column(Integer, ForeignKey("cuentas_zensoftware.id"), nullable=False)
    nombre = Column(String, default="Terminal sin nombre")
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    cuenta = relationship("CuentaZenSoftware", back_populates="terminales")