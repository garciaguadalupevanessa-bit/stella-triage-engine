# 🚐 Stella Triage Engine — Smart Camper Support & Fleet Governance

[![Language: ES](https://img.shields.io/badge/Idioma-Espa%C3%B1ol-blue.svg)](#-versión-en-español)
[![Language: EN](https://img.shields.io/badge/Language-English-green.svg)](#-english-version)

---

## 🌐 Quick Language Selector / Seleccionar Idioma

* [🇪🇸 **Ir a la versión en Español**](#-versión-en-español)
* [🇬🇧 **Jump to English Version**](#-english-version)

---

## 🇪🇸 Versión en Español

**Stella Triage Engine** es una plataforma integral de gestión de incidencias para flotas de camper vans inteligentes y ecológicas (*Stella Smart Camper*). El sistema combina la potencia de la inteligencia artificial generativa (**Google Gemini 1.5/2.0 Flash**) para el triaje automatizado en ruta con un flujo riguroso de gobernanza de flota, notificaciones en tiempo real vía **Resend API** y la simulación operativa de gestión de materiales e inventario mediante **SAP MM**.

### 🏗️ Arquitectura del Sistema

El proyecto está diseñado sobre una arquitectura limpia, asíncrona y modular basada en Python y FastAPI:

```text
stella-triage-engine/
├── app/
│   ├── routers/
│   │   ├── auth.py         # Endpoints y gestión de autenticación por roles
│   │   └── tickets.py      # Rutas REST de ciclo de vida de incidencias
│   ├── database.py         # Conexión SQLAlchemy y gestión de sesión (PostgreSQL / SQLite)
│   ├── models.py           # Modelos de entidad relacionales (Ticket, User, etc.)
│   ├── schemas.py          # Esquemas Pydantic para validación de entrada/salida
│   └── services.py         # Lógica de negocio: Gemini Cascade API y Resend Email Service
├── templates/
│   └── index.html          # Interfaz SPA responsiva en Tailwind CSS y Lucide Icons
├── main.py                 # Inicialización de FastAPI, montaje de estáticos y CORS
├── render.yaml             # Configuración de despliegue en Render Cloud
├── requirements.txt        # Dependencias de producción
└── README.md               # Documentación oficial del proyecto

⚡ Características Principales
Triaje Inteligente e Inmediato en Ruta (Gemini API Cascade):

Procesamiento de solicitudes de clientes mediante llamadas REST directas al motor de Google Gemini.

Sistema de Cascada (Cascade Fallback): Reintento automático ante endpoints de API (gemini-1.5-flash -> gemini-2.0-flash -> gemini-1.5-pro -> Motor de Reglas Local).

Asignación automática de categoría (MECÁNICA, ELÉCTRICA, HABITABILIDAD, OTROS), nivel de urgencia (ALTA, MEDIA, BAJA) y compromiso de respuesta (SLA de 24h, 48h o 72h).

Gobernanza, Auditoría y Service Desk (Vista Admin):

Acceso protegido por contraseña de auditoría (admin123).

Evaluación y validación de categorizaciones generadas por IA.

Flujo de aprobación para derivación a taller o rechazo justificado.

Panel Operativo Técnico e Integración SAP MM (Vista Tech):

Acceso restringido para el equipo de taller (tech123).

Generación de Solicitudes de Pedido de Recambios (SolPed SAP).

Simulación del flujo de entrada de mercancías y recepción de recambios con movimiento MIGO 101.

Notificaciones en Tiempo Real (Resend HTTPS API):

Envío de correos transaccionales formateados en HTML utilizando la API REST de Resend (puerto 443), superando los bloqueos de puertos SMTP tradicionales en entornos cloud.

Persistencia & Despliegue en la Nube:

PostgreSQL alojado en Render Cloud para almacenamiento persistente de tickets e historial de trazabilidad.

🛠️ Stack Tecnológico
Backend: Python 3.11, FastAPI, SQLAlchemy, Pydantic, Requests.

Base de Datos: PostgreSQL (Render) / SQLite (entorno de desarrollo local).

Inteligencia Artificial: Google Gemini REST API (v1beta).

Servicio de Correo: Resend REST API.

Frontend: HTML5, Tailwind CSS, Lucide Icons, JavaScript Async/Await.

Infraestructura Cloud: Render Web Services.

🚀 Instalación y Ejecución Local

1. Clonar el repositorio:

git clone [https://github.com/tu-usuario/stella-triage-engine.git](https://github.com/tu-usuario/stella-triage-engine.git)
cd stella-triage-engine

2. Activar el entorno vitual:

   Powershell (Windows):

   .\.venv\Scripts\Activate.ps1

   Bash (Linux/macOS):

   source .venv/bin/activate

3. Instalar dependencias:

   pip install -r requirements.txt

4. Configurar variables de entorno (.env):

   DATABASE_URL=sqlite:///./stella_triage.db
   GEMINI_API_KEY=tu_gemini_api_key
   RESEND_API_KEY=tu_resend_api_key

5. Inciar el servidor de desarrollo:

   uvicorn main:app --reload

   Accede a la aplicación en http://127.0.0.1:8000.


| Perfil de Usuario | Pestaña de la App | Contraseña de Acceso |
| :--- | :--- | :--- |
| **Cliente / Usuario** | Notificar Incidencia | *Acceso Público* |
| **Administrador / Flota** | Gobernanza Flota | `admin123` |
| **Técnico / Taller** | Técnico & SAP MM | `tech123` |


🇬🇧 English Version
Stella Triage Engine is a comprehensive incident management platform for smart and eco-friendly camper van fleets (Stella Smart Camper). The system combines the power of generative artificial intelligence (Google Gemini 1.5/2.0 Flash) for automated roadside triage with a rigorous fleet governance workflow, real-time email notifications via Resend API, and operational inventory and materials management simulation powered by SAP MM.

🏗️ System Architecture
The project is built upon a clean, asynchronous, and modular architecture using Python and FastAPI:

stella-triage-engine/
├── app/
│   ├── routers/
│   │   ├── auth.py         # Endpoints & role-based authentication management
│   │   └── tickets.py      # Incident lifecycle REST routes
│   ├── database.py         # SQLAlchemy connection & session handling (PostgreSQL / SQLite)
│   ├── models.py           # Relational entity models (Ticket, User, etc.)
│   ├── schemas.py          # Pydantic schemas for input/output validation
│   └── services.py         # Business logic: Gemini Cascade API & Resend Email Service
├── templates/
│   └── index.html          # Responsive SPA UI with Tailwind CSS & Lucide Icons
├── main.py                 # FastAPI initialization, static mounting & CORS
├── render.yaml             # Render Cloud deployment blueprint
├── requirements.txt        # Production dependencies
└── README.md               # Official project documentation

⚡ Key Features
Intelligent & Immediate Roadside Triage (Gemini API Cascade):

Processes customer requests via direct REST calls to Google Gemini engine.

Cascade Fallback Mechanism: Automated retry across API endpoints (gemini-1.5-flash -> gemini-2.0-flash -> gemini-1.5-pro -> Local Rule Engine).

Automated category assignment (MECHANICAL, ELECTRICAL, HABITABILITY, OTHERS), urgency level (HIGH, MEDIUM, LOW), and Service Level Agreement commitment (24h, 48h, or 72h SLA).

Fleet Governance, Auditability & Service Desk (Admin View):

Audit password-protected access (admin123).

Review and validation of AI-generated incident classifications.

Approval workflow to dispatch tickets to technical workshop or issue justified rejections.

Technical Operational Panel & SAP MM Integration (Tech View):

Restricted access for workshop technical staff (tech123).

Generation of SAP Purchase Requisitions (SAP SolPed).

Simulation of Goods Receipt and spare parts inventory management using movement type MIGO 101.

Real-Time Notifications (Resend HTTPS API):

Transmits HTML-formatted emails using Resend REST API (port 443), bypassing cloud provider SMTP port restrictions.

Persistence & Cloud Deployment:

PostgreSQL database hosted on Render Cloud for persistent ticket storage and traceability logs.

🛠️ Tech Stack
Backend: Python 3.11, FastAPI, SQLAlchemy, Pydantic, Requests.

Database: PostgreSQL (Render) / SQLite (Local development).

Artificial Intelligence: Google Gemini REST API (v1beta).

Email Service: Resend REST API.

Frontend: HTML5, Tailwind CSS, Lucide Icons, JavaScript Async/Await.

Cloud Infrastructure: Render Web Services.

🚀 Local Installation & Setup

1. Clone the repository:
   git clone [https://github.com/tu-usuario/stella-triage-engine.git](https://github.com/tu-usuario/stella-triage-engine.git)
cd stella-triage-engine

2. Activate virtual environment:

   On PowerShell (Windows):
   .\.venv\Scripts\Activate.ps1

   On Linux/macOS:
   source .venv/bin/activate

3.  Install dependencies:

   pip install -r requirements.txt

4. Configure environment variables (.env):

   DATABASE_URL=sqlite:///./stella_triage.db
   GEMINI_API_KEY=your_gemini_api_key
   RESEND_API_KEY=your_resend_api_key

5. Run local server: 

   uvicorn main:app --reload
   Access the web application at http://127.0.0.1:8000.

 | User Profile | App Tab | Access Password |
| :--- | :--- | :--- |
| **Customer / User** | Notificar Incidencia | *Public Access* |
| **Administrator / Fleet** | Gobernanza Flota | `admin123` |
| **Technician / Workshop** | Técnico & SAP MM | `tech123` |  





