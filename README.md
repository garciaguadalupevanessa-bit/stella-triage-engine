# Stella Triage Engine 🚗⚡

**[ES]** Motor de triaje, clasificación y gestión del ciclo de vida de incidencias asistido por IA para el ecosistema Stella. Integra verificación humana (Admin), gestión técnica y conexión simulada con compras de **SAP MM** (SolPed / Entrada de Mercancías).

**[EN]** AI-powered triage, classification, and incident lifecycle management engine built for the Stella ecosystem. Integrates human-in-the-loop review (Admin), technical intervention, and simulated **SAP MM** procurement integration (Purchase Requisitions / Goods Receipts).

---

## 🚀 Features / Características

- **[ES]** Clasificación automática de peticiones en tiempo real con IA / Reglas.
- **[ES]** Evaluación estricta de datos de entrada mediante esquemas Pydantic.
- **[ES]** Verificación humana en el bucle (Human-in-the-loop) para aprobación de Administrador.
- **[ES]** Gestión de resolución técnica y emisión simulada de SolPed / Pedidos en SAP MM.
- **[EN]** Real-time automated query classification via AI / Rules.
- **[EN]** Strict payload validation via Pydantic schemas.
- **[EN]** Human-in-the-loop review interface for Admin approval.
- **[EN]** Technical resolution management and simulated SAP MM Purchase Requisition workflow.

---

## 🛠️ Tech Stack / Tecnologías

* **Language / Lenguaje:** Python 3.11+
* **Framework:** FastAPI
* **Data Validation / Validación:** Pydantic
* **ORM & Database / Base de Datos:** SQLAlchemy + SQLite / PostgreSQL
* **ERP Integration / Integración ERP:** SAP MM (Purchase Requisition / Goods Receipt Mock)
* **AI Engine / Motor de IA:** Groq / OpenAI API (Structured Outputs)
* **Frontend UI:** Lovable / Streamlit

---

## 🔄 Workflow & Roles / Flujo de Trabajo y Roles

```text
[1. User/Client]       ---> Submits Complaint/Query (POST /tickets)
                                | (Initial Status: PENDING_ADMIN_REVIEW)
[2. Admin Review]      ---> Approves/Updates Category & Urgency (PATCH /tickets/{id}/review)
                                | (New Status: ASSIGNED_TO_TECHNICAL)
[3. Technical Dept]    ---> Evaluates Action (POST /tickets/{id}/action)
                                |
                                +---> Option A: Direct Fix (Status: RESOLVED)
                                |
                                +---> Option B: Order Replacement Parts 
                                      ---> Generates SAP MM SolPed (Status: AWAITING_SAP_STOCK)
                                      ---> Simulates Goods Receipt (MIGO 101) ---> (Status: RESOLVED)

# API Endpoints / Rutas de la API

| Method | Endpoint | Role / Component | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/System` | Health check | Estado del servicio |
| `POST` | `/tickets` | User / Cliente | Create a new triage ticket / Crear incidencia |
| `GET` | `/tickets` | Admin / Tech | List all tickets with optional status filtering / Listar tickets |
| `PATCH` | `/tickets/{id}/review` | Admin | Review & approve triage / Verificación humana del Admin |
| `POST` | `/tickets/{id}/action` | Tech / SAP MM | Resolve ticket or initiate SAP Purchase Requisition / Acción técnica y SAP |

⚙️ Quickstart / Inicio Rápido

# Clone repository / Clonar repositorio
git clone [https://github.com/garciaguadalupevanessa-bit/stella-triage-engine.git](https://github.com/garciaguadalupevanessa-bit/stella-triage-engine.git)

# Install dependencies / Instalar dependencias
pip install -r requirements.txt

# Seed database / Poblar base de datos sintética
python seed_data.py

# Run FastAPI server / Ejecutar servidor FastAPI
uvicorn main:app --reload

📊 Database Schema / Esquema de Datos
SQLite / PostgreSQL via SQLAlchemy

Ticket Model: id, user_id, query, category, urgency, department, summary, status, sap_solped_id, sap_material_id, sap_status, created_at, updated_at.

git add README.md database.py models.py seed_data.py .gitignore requirements.txt