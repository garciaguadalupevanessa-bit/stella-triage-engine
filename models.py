from sqlalchemy import Column, Integer, String, Text, DateTime, func
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
    
    # Workflow Status
    # Options: PENDING_ADMIN_REVIEW, ASSIGNED_TO_TECHNICAL, RESOLVED, AWAITING_SAP_STOCK
    status = Column(String(50), default="PENDING_ADMIN_REVIEW")
    
    # SAP MM Integration Fields
    sap_solped_id = Column(String(50), nullable=True)     # SolPed
    sap_material_id = Column(String(50), nullable=True)   # Material Number
    sap_status = Column(String(50), nullable=True)        # e.g., CREATED, GOODS_RECEIVED_MIGO_101
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    