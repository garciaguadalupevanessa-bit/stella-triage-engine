from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Stella Triage Engine",
    description="Motor de triaje y clasificación asistido por IA",
    version="0.1.0"
)

# Modelo Pydantic para la solicitud de entrada
class TriageRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

# Modelo Pydantic para la respuesta de salida
class TriageResponse(BaseModel):
    category: str
    urgency: str
    department: str
    summary: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Stella Triage Engine running"}