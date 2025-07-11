# app/database/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Obtener la URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para declarar modelos
Base = declarative_base()

# Función global para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------
# ⚙️ Función para crear todas las tablas
# ---------------------------------------------
def init_db():
    from app.models.cuenta_zensoftware import CuentaZenSoftware
    from app.models.verificacion_pendiente import VerificacionPendiente
    from app.models.terminal import Terminal  # ✅ Asegúrate de que este archivo exista y esté bien definido

    Base.metadata.create_all(bind=engine)