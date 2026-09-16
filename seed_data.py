from app.database import SessionLocal, engine, Base
from app.models import TicketModel

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Clean existing data / Limpiar datos existentes
    db.query(TicketModel).delete()
    
    synthetic_tickets = [
        TicketModel(
            user_id="usr_101",
            query="La pantalla del cuadro de mandos no enciende al arrancar el vehículo.",
            category="Software Issue / Incidencia Software",
            urgency="MEDIUM / MEDIA",
            department="IT Support / Soporte Técnico",
            summary="Pantalla principal no responde tras encendido.",
            status="PENDING_ADMIN_REVIEW"
        ),
        TicketModel(
            user_id="usr_102",
            query="Ruido metálico en los frenos traseros al frenar en pendiente.",
            category="Mechanical Hazard / Peligro Mecánico",
            urgency="HIGH / ALTA",
            department="Roadside Assistance / Asistencia en Carretera",
            summary="Posible desgaste grave de pastillas/discos de freno.",
            status="ASSIGNED_TO_TECHNICAL"
        ),
        TicketModel(
            user_id="usr_103",
            query="Necesitamos sustituir el módulo de gestión de batería auxiliar averiado.",
            category="Hardware Replacement / Recambio de Pieza",
            urgency="HIGH / ALTA",
            department="Technical Maintenance / Mantenimiento Técnico",
            summary="Avería en módulo de batería. Requiere pedido de repuesto.",
            status="AWAITING_SAP_STOCK",
            sap_solped_id="10004821",
            sap_material_id="MAT-BAT-12V-X",
            sap_status="PURCHASE_REQUISITION_CREATED"
        )
    ]
    
    db.add_all(synthetic_tickets)
    db.commit()
    db.close()
    print("✅ Synthetic tickets seeded successfully into SQLite!")

if __name__ == "__main__":
    seed_database()