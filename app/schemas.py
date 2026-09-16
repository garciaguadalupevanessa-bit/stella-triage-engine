from pydantic import BaseModel, ConfigDict
from typing import Optional

class TicketCreate(BaseModel):
    query: str
    customer_email: str
    van_license_plate: str
    customer_name: Optional[str] = "Cliente Stella"
    customer_phone: Optional[str] = "No facilitado"
    location: Optional[str] = "En ruta (Ubicación no enviada)"

class AdminReview(BaseModel):
    category: Optional[str] = None
    urgency: Optional[str] = None
    department: Optional[str] = None
    approved: bool = True
    rejection_reason: Optional[str] = None

class TechnicalAction(BaseModel):
    action_type: str  # "RESOLVE" o "REQUEST_PARTS"
    resolution_notes: Optional[str] = None
    material_id: Optional[str] = None

class TicketResponse(BaseModel):
    id: int
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    van_license_plate: Optional[str] = None
    location: Optional[str] = None
    query: str
    category: Optional[str] = None
    urgency: Optional[str] = None
    department: Optional[str] = None
    summary: Optional[str] = None
    estimated_sla: Optional[str] = None
    status: str
    sap_solped_id: Optional[str] = None
    sap_material_id: Optional[str] = None
    sap_status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    role: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    role: str
    message: str