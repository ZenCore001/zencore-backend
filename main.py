# app/models/main.py o main.py raíz
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal

# 🔽 Importa el router
from app.routes import cuenta

app = FastAPI()

# Incluir los routers
app.include_router(cuenta.router)

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"ZenCore": "Backend activo 🚀"}

# Ruta de prueba de conexión
@app.get("/check-db")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {"estado": "Conexión exitosa a la base de datos"}
    except Exception as e:
        return {"error": str(e)}