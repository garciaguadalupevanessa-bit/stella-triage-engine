from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import random
import os
import json
import google.generativeai as genai

from database import engine, get_db, Base
from models import TicketModel

# Inicializar tablas de la Base de Datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stella Triage Engine",
    description="AI-powered triage using Gemini, lifecycle management, and SAP MM integration",
    version="0.2.0"
)

# Configuración de Plantillas HTML
templates = Jinja2Templates(directory="templates")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar cliente de Google Gemini
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# --- Schemas Pydantic ---

class TicketCreate(BaseModel):
    query: str
    user_id: Optional[str] = "usr_guest"

class AdminReview(BaseModel):
    category: Optional[str] = None
    urgency: Optional[str] = None
    department: Optional[str] = None
    approved: bool = True

class TechnicalAction(BaseModel):
    action_type: str  # Opción: "RESOLVE" o "REQUEST_PARTS"
    resolution_notes: Optional[str] = None
    material_id: Optional[str] = None

class TicketResponse(BaseModel):
    id: int
    user_id: Optional[str] = None
    query: str
    category: Optional[str] = None
    urgency: Optional[str] = None
    department: Optional[str] = None
    summary: Optional[str] = None
    status: str
    sap_solped_id: Optional[str] = None
    sap_material_id: Optional[str] = None
    sap_status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# --- Clasificador Inteligente con LLM (Google Gemini) ---

def classify_query(query: str) -> dict:
    prompt = f"""
    Eres el motor de triaje inteligente de Stella Triage Engine.
    Analiza la incidencia enviada por el usuario y clasifícala devolviendo ÚNICAMENTE un objeto JSON válido con la siguiente estructura:
    {{
      "category": "Categoría técnica del problema (Ej: Peligro Mecánico, Incidencia Software, Climatización, Almacén, etc.)",
      "urgency": "HIGH / ALTA, MEDIUM / MEDIA o LOW / BAJA",
      "department": "Departamento asignado para resolución (Ej: Asistencia en Carretera, Soporte IT, Mantenimiento, Almacén)",
      "summary": "Resumen técnico sintético del problema en máximo 20 palabras"
    }}

    Incidencia enviada por el usuario: "{query}"
    """

    if GEMINI_KEY:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            return {
                "category": data.get("category", "General Inquiry / Consulta General"),
                "urgency": data.get("urgency", "MEDIUM / MEDIA"),
                "department": data.get("department", "Support / Soporte Técnico"),
                "summary": data.get("summary", f"Gemini Triage: {query[:40]}...")
            }
        except Exception as e:
            print(f"Error llamando a la API de Gemini: {e}")

    # Fallback heurístico de seguridad si la API no estuviera configurada
    query_lower = query.lower()
    if any(word in query_lower for word in ["batería", "freno", "motor", "fuego", "peligro", "brake", "battery"]):
        return {
            "category": "Mechanical Hazard / Peligro Mecánico",
            "urgency": "HIGH / ALTA",
            "department": "Roadside Assistance / Asistencia en Carretera",
            "summary": f"Fallback Triage (Crítico): {query[:40]}..."
        }
    return {
        "category": "General Inquiry / Consulta General",
        "urgency": "MEDIUM / MEDIA",
        "department": "IT Support / Soporte Técnico",
        "summary": f"Fallback Triage: {query[:40]}..."
    }

# --- Endpoints API & Frontend ---

# 0. FRONTEND UI: Servir Dashboard
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# 1. USER: Crear Ticket con Triaje IA
@app.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    triage_info = classify_query(payload.query)
    
    new_ticket = TicketModel(
        user_id=payload.user_id,
        query=payload.query,
        category=triage_info["category"],
        urgency=triage_info["urgency"],
        department=triage_info["department"],
        summary=triage_info["summary"],
        status="PENDING_ADMIN_REVIEW"
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

# 2. GLOBAL: Listar Tickets
@app.get("/tickets", response_model=List[TicketResponse])
def get_tickets(status_filter: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(TicketModel)
    if status_filter:
        query = query.filter(TicketModel.status == status_filter)
    return query.all()

# 3. ADMIN: Human Review
@app.patch("/tickets/{ticket_id}/review", response_model=TicketResponse)
def admin_review_ticket(ticket_id: int, review: AdminReview, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if review.category:
        setattr(ticket, "category", review.category)
    if review.urgency:
        setattr(ticket, "urgency", review.urgency)
    if review.department:
        setattr(ticket, "department", review.department)
        
    setattr(ticket, "status", "ASSIGNED_TO_TECHNICAL" if review.approved else "REJECTED_BY_ADMIN")
    db.commit()
    db.refresh(ticket)
    return ticket

# 4. TECH / SAP MM: Acción Técnica
@app.post("/tickets/{ticket_id}/action", response_model=TicketResponse)
def technical_action(ticket_id: int, action: TechnicalAction, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    current_summary = str(getattr(ticket, "summary") or "")
    
    if action.action_type == "RESOLVE":
        setattr(ticket, "status", "RESOLVED")
        setattr(ticket, "summary", current_summary + f" | Resolucion: {action.resolution_notes or 'Reparado directamente.'}")
    
    elif action.action_type == "REQUEST_PARTS":
        solped_number = f"1000{random.randint(4000, 9999)}"
        mat_id = action.material_id or "MAT-STD-REPLACEMENT"
        
        setattr(ticket, "status", "AWAITING_SAP_STOCK")
        setattr(ticket, "sap_solped_id", solped_number)
        setattr(ticket, "sap_material_id", mat_id)
        setattr(ticket, "sap_status", "PURCHASE_REQUISITION_CREATED")
        setattr(ticket, "summary", current_summary + f" | SAP SolPed: #{solped_number} para Material {mat_id}")
    else:
        raise HTTPException(status_code=400, detail="Acción no válida.")
    
    db.commit()
    db.refresh(ticket)
    return ticket

# 5. SAP MM: Entrada de Mercancía MIGO 101
@app.post("/tickets/{ticket_id}/sap-goods-receipt", response_model=TicketResponse)
def sap_goods_receipt(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if getattr(ticket, "status") != "AWAITING_SAP_STOCK":
        raise HTTPException(status_code=400, detail="El ticket no está esperando stock")
    
    current_summary = str(getattr(ticket, "summary") or "")
    setattr(ticket, "sap_status", "GOODS_RECEIVED_MIGO_101")
    setattr(ticket, "status", "RESOLVED")
    setattr(ticket, "summary", current_summary + " | Recepcion SAP MIGO (Mov. 101) completada. Ticket cerrado.")
    
    db.commit()
    db.refresh(ticket)
    return ticket