from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from app.database import Base

class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Datos obligatorios del cliente/van
    customer_name = Column(String, nullable=True)
    customer_email = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)
    van_license_plate = Column(String, nullable=False)
    location = Column(String, nullable=True)

    # Detalle de la incidencia
    query = Column(Text, nullable=False)

    # Clasificación Gemini IA
    category = Column(String, nullable=True)
    urgency = Column(String, nullable=True)
    department = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    estimated_sla = Column(String, nullable=True) # Tiempo estimado de solución

    # Gobernanza y SAP MM
    status = Column(String, default="PENDING_ADMIN_REVIEW")
    sap_solped_id = Column(String, nullable=True)
    sap_material_id = Column(String, nullable=True)
    sap_status = Column(String, nullable=True)
    