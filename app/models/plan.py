# app/models/plan.py
from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database.db import Base

class Plan(Base):
    __tablename__ = "planes"

    id = Column(Integer, primary_key=True, index=True) #Auto-incrementable
    nombre = Column(String, unique=True, nullable=False) #Ej: PRO, BÁSICO, etc.
    descripcion = Column(String, nullable=True) #	Texto corto opcional
    precio_mensual = Column(Float, nullable=False) #Solo cobro mensual
    usuarios_incluidos = Column(Integer, nullable=False) #	Cuántos usuarios permite el plan
    terminales_incluidas = Column(Integer, nullable=False) #	Cuántas PCs pueden conectarse
    estatus = Column(String, nullable=False, default="activo")  # activo / inactivo
    es_personalizado = Column(Boolean, default=False) #	Plan hecho a la medida