from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI application / Inicializar la aplicación FastAPI
app = FastAPI(
    title="Stella Triage Engine",
    description="AI-powered triage and classification engine / Motor de triaje y clasificación asistido por IA",
    version="0.1.0"
)

# Pydantic model for incoming request / Modelo Pydantic para la solicitud de entrada
class TriageRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

# Pydantic model for structured response / Modelo Pydantic para la respuesta estructurada
class TriageResponse(BaseModel):
    category: str
    urgency: str
    department: str
    summary: str

# Helper logic to classify queries / Lógica auxiliar para clasificar consultas
def classify_triage_query(query: str) -> TriageResponse:
    query_lower = query.lower()
    
    # Urgency & Category keyword rules / Reglas de palabras clave para urgencia y categoría
    if any(word in query_lower for word in ["batería", "freno", "motor", "fuego", "danger", "brake", "battery"]):
        return TriageResponse(
            category="Mechanical Hazard / Peligro Mecánico",
            urgency="HIGH / ALTA",
            department="Roadside Assistance / Asistencia en Carretera",
            summary=f"Critical issue reported: {query[:30]}..."
        )
    elif any(word in query_lower for word in ["app", "pantalla", "error", "login", "password"]):
        return TriageResponse(
            category="Software Issue / Incidencia Software",
            urgency="MEDIUM / MEDIA",
            department="IT Support / Soporte Técnico",
            summary=f"App error logged: {query[:30]}..."
        )
    else:
        return TriageResponse(
            category="General Inquiry / Consulta General",
            urgency="LOW / BAJA",
            department="Customer Care / Atención al Cliente",
            summary=f"Standard inquiry: {query[:30]}..."
        )

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Stella Triage Engine is running properly"}

# POST Endpoint for triage classification / Endpoint POST para clasificación de triaje
@app.post("/triage", response_model=TriageResponse)
def evaluate_triage(payload: TriageRequest):
    return classify_triage_query(payload.query)