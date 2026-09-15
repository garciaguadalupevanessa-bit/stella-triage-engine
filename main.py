from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import random

from database import engine, get_db, Base
from models import TicketModel

# Initialize Database Tables / Inicializar tablas de BD
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stella Triage Engine",
    description="AI-powered triage, lifecycle management, and SAP MM integration / Motor de triaje y gestión de incidencias con SAP MM",
    version="0.2.0"
)

# --- Configuración de Plantillas / Templates ---
templates = Jinja2Templates(directory="templates")


# --- CORS Middleware / Configuración de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (Lovable, localhost, etc.)
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PATCH, OPTIONS, etc.
    allow_headers=["*"],
)

# --- Ruta Raíz / Frontend UI ---
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# --- Pydantic Schemas / Esquemas Pydantic ---

class TicketCreate(BaseModel):
    query: str
    user_id: Optional[str] = "usr_guest"

class AdminReview(BaseModel):
    category: Optional[str] = None
    urgency: Optional[str] = None
    department: Optional[str] = None
    approved: bool = True

class TechnicalAction(BaseModel):
    action_type: str  # Options: "RESOLVE" or "REQUEST_PARTS"
    resolution_notes: Optional[str] = None
    material_id: Optional[str] = None  # Needed if REQUEST_PARTS

class TicketResponse(BaseModel):
    id: int
    user_id: Optional[str]
    query: str
    category: Optional[str]
    urgency: Optional[str]
    department: Optional[str]
    summary: Optional[str]
    status: str
    sap_solped_id: Optional[str]
    sap_material_id: Optional[str]
    sap_status: Optional[str]

    class Config:
        from_attributes = True

# --- Classification Helper / Lógica de Clasificación Inicial ---

def classify_query(query: str):
    query_lower = query.lower()
    if any(word in query_lower for word in ["batería", "freno", "motor", "fuego", "danger", "brake", "battery"]):
        return {
            "category": "Mechanical Hazard / Peligro Mecánico",
            "urgency": "HIGH / ALTA",
            "department": "Roadside Assistance / Asistencia en Carretera",
            "summary": f"Critical issue: {query[:40]}..."
        }
    elif any(word in query_lower for word in ["app", "pantalla", "error", "login", "password"]):
        return {
            "category": "Software Issue / Incidencia Software",
            "urgency": "MEDIUM / MEDIA",
            "department": "IT Support / Soporte Técnico",
            "summary": f"Software error: {query[:40]}..."
        }
    else:
        return {
            "category": "General Inquiry / Consulta General",
            "urgency": "LOW / BAJA",
            "department": "Customer Care / Atención al Cliente",
            "summary": f"Standard inquiry: {query[:40]}..."
        }

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Stella Triage Engine v0.2.0 is running with SQL & SAP MM support"}

# 1. USER: Create Ticket / Crear Incidencia
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

# 2. GLOBAL/ADMIN: List Tickets / Listar Incidencias
@app.get("/tickets", response_model=List[TicketResponse])
def get_tickets(status_filter: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(TicketModel)
    if status_filter:
        query = query.filter(TicketModel.status == status_filter)
    return query.all()

# 3. ADMIN: Human Review / Verificación Humana del Admin
@app.patch("/tickets/{ticket_id}/review", response_model=TicketResponse)
def admin_review_ticket(ticket_id: int, review: AdminReview, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if review.category:
        ticket.category = review.category
    if review.urgency:
        ticket.urgency = review.urgency
    if review.department:
        ticket.department = review.department
        
    ticket.status = "ASSIGNED_TO_TECHNICAL" if review.approved else "REJECTED_BY_ADMIN"
    db.commit()
    db.refresh(ticket)
    return ticket

# 4. TECH / SAP MM: Technical Action / Acción Técnica y Pedido SAP
@app.post("/tickets/{ticket_id}/action", response_model=TicketResponse)
def technical_action(ticket_id: int, action: TechnicalAction, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if action.action_type == "RESOLVE":
        ticket.status = "RESOLVED"
        ticket.summary += f" | Resolution: {action.resolution_notes or 'Resolved directly by technician.'}"
    
    elif action.action_type == "REQUEST_PARTS":
        # Simulate SAP MM Purchase Requisition (SolPed) creation
        solped_number = f"1000{random.randint(4000, 9999)}"
        mat_id = action.material_id or "MAT-STD-REPLACEMENT"
        
        ticket.status = "AWAITING_SAP_STOCK"
        ticket.sap_solped_id = solped_number
        ticket.sap_material_id = mat_id
        ticket.sap_status = "PURCHASE_REQUISITION_CREATED"
        ticket.summary += f" | SAP SolPed generated: #{solped_number} for Material {mat_id}"
    else:
        raise HTTPException(status_code=400, detail="Invalid action_type. Choose RESOLVE or REQUEST_PARTS.")
    
    db.commit()
    db.refresh(ticket)
    return ticket

# 5. SAP MM MOCK: Goods Receipt (MIGO 101) / Simulación de Recepción de Mercancía
@app.post("/tickets/{ticket_id}/sap-goods-receipt", response_model=TicketResponse)
def sap_goods_receipt(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if ticket.status != "AWAITING_SAP_STOCK":
        raise HTTPException(status_code=400, detail="Ticket is not awaiting SAP stock")
    
    ticket.sap_status = "GOODS_RECEIVED_MIGO_101"
    ticket.status = "RESOLVED"
    ticket.summary += " | Stock received via SAP MIGO (Mov. 101). Ticket closed."
    
    db.commit()
    db.refresh(ticket)
    return ticket
