import random
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TicketModel
from app.schemas import TicketCreate, AdminReview, TechnicalAction, TicketResponse
from app.services import classify_query, send_status_email

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    triage_info = classify_query(payload.query)
    
    new_ticket = TicketModel(
        customer_name=payload.customer_name,
        customer_email=payload.customer_email,
        customer_phone=payload.customer_phone,
        van_license_plate=payload.van_license_plate,
        location=payload.location,
        query=payload.query,
        category=triage_info["category"],
        urgency=triage_info["urgency"],
        department=triage_info["department"],
        summary=triage_info["summary"],
        estimated_sla=triage_info["estimated_sla"],
        status="PENDING_ADMIN_REVIEW"
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    # Email de recepción
    email_body = f"""
    <h2>Stella Smart Camper - Incidencia #{new_ticket.id} Registrada</h2>
    <p>Hola <strong>{new_ticket.customer_name}</strong>, hemos recibido tu notificación para la Van <strong>{new_ticket.van_license_plate}</strong>.</p>
    <ul>
        <li><strong>Categoría IA:</strong> {new_ticket.category}</li>
        <li><strong>Urgencia:</strong> {new_ticket.urgency}</li>
        <li><strong>Tiempo Estimado (SLA):</strong> {new_ticket.estimated_sla}</li>
    </ul>
    <p>Nuestro equipo de flota está gestionando tu solicitud.</p>
    """
    
    recipient = str(getattr(new_ticket, "customer_email", payload.customer_email))
    background_tasks.add_task(send_status_email, recipient, f"Incidencia #{new_ticket.id} Registrada", email_body)

    return new_ticket


@router.get("", response_model=List[TicketResponse])
def get_tickets(status_filter: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(TicketModel)
    if status_filter:
        query = query.filter(TicketModel.status == status_filter)
    return query.all()

@router.patch("/{ticket_id}/review", response_model=TicketResponse)
def admin_review_ticket(ticket_id: int, review: AdminReview, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    if review.category:
        setattr(ticket, "category", review.category)
    if review.urgency:
        setattr(ticket, "urgency", review.urgency)
    if review.department:
        setattr(ticket, "department", review.department)
        
    current_summary = str(getattr(ticket, "summary") or "")

    if review.approved:
        setattr(ticket, "status", "ASSIGNED_TO_TECHNICAL")
    else:
        setattr(ticket, "status", "REJECTED_BY_ADMIN")
        reason = review.rejection_reason or "No procede según políticas de garantía/alquiler."
        setattr(ticket, "summary", current_summary + f" | RECHAZADO: {reason}")

    db.commit()
    db.refresh(ticket)
    return ticket

@router.post("/{ticket_id}/action", response_model=TicketResponse)
def technical_action(ticket_id: int, action: TechnicalAction, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    current_summary = str(getattr(ticket, "summary") or "")
    
    if action.action_type == "RESOLVE":
        setattr(ticket, "status", "RESOLVED")
        setattr(ticket, "summary", current_summary + f" | Resolución: {action.resolution_notes or 'Reparado en taller/ruta.'}")
    
    elif action.action_type == "REQUEST_PARTS":
        solped_number = f"1000{random.randint(4000, 9999)}"
        mat_id = action.material_id or "MAT-VAN-ECO-PARTS"
        
        setattr(ticket, "status", "AWAITING_SAP_STOCK")
        setattr(ticket, "sap_solped_id", solped_number)
        setattr(ticket, "sap_material_id", mat_id)
        setattr(ticket, "sap_status", "PURCHASE_REQUISITION_CREATED")
        setattr(ticket, "estimated_sla", "Afectado por stock Almacén Central (+24/48h)")
        setattr(ticket, "summary", current_summary + f" | SAP SolPed: #{solped_number} enviada a Almacén Central")

        # Email actualización SAP
        email_body = f"""
        <h2>Stella Smart Camper - Solicitud de Recambio SAP MM</h2>
        <p>Tu incidencia <strong>#{ticket.id}</strong> para la Van <strong>{ticket.van_license_plate}</strong> requiere un repuesto original.</p>
        <p>Se ha generado la SolPed SAP <strong>#{solped_number}</strong> a nuestro Almacén Central.</p>
        <p><strong>Nuevo Plazo SLA:</strong> {ticket.estimated_sla}</p>
        """
        background_tasks.add_task(send_status_email, getattr(ticket, "customer_email"), f"Actualización Incidencia #{ticket.id} - SAP Stock", email_body)
    else:
        raise HTTPException(status_code=400, detail="Acción no válida.")
    
    db.commit()
    db.refresh(ticket)
    return ticket

@router.post("/{ticket_id}/sap-goods-receipt", response_model=TicketResponse)
def sap_goods_receipt(ticket_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    if getattr(ticket, "status") != "AWAITING_SAP_STOCK":
        raise HTTPException(status_code=400, detail="El ticket no está esperando stock")
    
    current_summary = str(getattr(ticket, "summary") or "")
    setattr(ticket, "sap_status", "GOODS_RECEIVED_MIGO_101")
    setattr(ticket, "status", "RESOLVED")
    setattr(ticket, "summary", current_summary + " | Recepción SAP MIGO 101 completada. Incidencia cerrada.")
    
    db.commit()
    db.refresh(ticket)

    # Email de cierre
    email_body = f"""
    <h2>Stella Smart Camper - Incidencia Resuelta</h2>
    <p>La incidencia <strong>#{ticket.id}</strong> para la Van <strong>{ticket.van_license_plate}</strong> ha sido completamente resuelta tras el movimiento MIGO 101 en SAP MM.</p>
    <p>¡Gracias por confiar en Stella Smart Camper!</p>
    """
    background_tasks.add_task(send_status_email, getattr(ticket, "customer_email"), f"Incidencia #{ticket.id} Resuelta", email_body)

    return ticket