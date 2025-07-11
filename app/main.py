from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal

app = FastAPI()

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta raíz para confirmar que el servidor está en línea
@app.get("/")
def root():
    return {"mensaje": "Servidor ZenCore en línea ✅"}

# Ruta de prueba para verificar la conexión a la base de datos
@app.get("/check-db")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {"estado": "Conexión exitosa a la base de datos"}
    except Exception as e:
        return {"error": str(e)}