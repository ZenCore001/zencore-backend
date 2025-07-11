# crear_tablas.py
from app.database.db import engine, Base
from app.models.verificacion_pendiente import VerificacionPendiente
from app.models.cuenta_zensoftware import CuentaZenSoftware

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas exitosamente.")