# init_db.py
from app.database.db import engine, Base
from app.models import cuenta_zensoftware, verificacion_pendiente, terminal

# Crear todas las tablas declaradas en los modelos importados
Base.metadata.create_all(bind=engine)

print("✅ Tablas creadas correctamente.")