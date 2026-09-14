from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=True)
    query = Column(Text, nullable=False)
    
    # AI / Triage Initial Output
    category = Column(String(100), nullable=True)
    urgency = Column(String(50), nullable=True)
    department = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
    
    # Workflow Status / Estado del Flujo de Trabajo
    # Options: PENDING_ADMIN_REVIEW, ASSIGNED_TO_TECHNICAL, RESOLVED, AWAITING_SAP_STOCK
    status = Column(String(50), default="PENDING_ADMIN_REVIEW")
    
    # SAP MM Integration Fields / Campos de Integración SAP MM
    sap_solped_id = Column(String(50), nullable=True)     # Purchase Requisition / SolPed
    sap_material_id = Column(String(50), nullable=True)   # Material Number
    sap_status = Column(String(50), nullable=True)        # e.g., CREATED, GOODS_RECEIVED
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)