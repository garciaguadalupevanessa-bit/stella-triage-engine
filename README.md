# 🚐 Stella Triage Engine — Smart Camper Support & Fleet Governance

<p align="center">
  <img src="https://raw.githubusercontent.com/garciaguadalupevanessa-bit/stella-triage-engine/main/static/logo.png" alt="Stella Triage Engine Logo" width="220" />
</p>

<p align="center">
  <a href="#es"><b>🇪🇸 Leer en Español</b></a> | 
  <a href="#en"><b>🇬🇧 Read in English</b></a>
</p>

---

---

<a id="es"></a>
## 🇪🇸 Versión en Español

**Stella Triage Engine** es una plataforma de software integral de grado empresarial diseñada para la gestión de incidencias, triaje automatizado con Inteligencia Artificial Generativa y gobernanza operativa de la flota de camper vans ecológicas **Stella Smart Camper**.

El sistema conecta el soporte en ruta en tiempo real para clientes con los flujos de auditoría de gobernanza y la gestión técnica de materiales e inventario simulando el ecosistema **SAP MM (Materials Management)**.

---

### 🌐 Despliegue en la Nube (Producción)

El proyecto se encuentra desplegado y plenamente operativo en la infraestructura cloud de **Render**:

* 🔗 **URL de la Aplicación en Vivo**: `https://stella-triage-engine.onrender.com`
* 🗄️ **Base de Datos Persistente**: PostgreSQL Cloud Managed Instance
* ✉️ **Servicio de Notificaciones**: Resend HTTPS REST API (Puerto 443)

---

### 🏗️ Arquitectura y Estructura del Proyecto

```text
stella-triage-engine/
├── app/
│   ├── routers/
│   │   ├── auth.py         # Autenticación y control de acceso por roles
│   │   └── tickets.py      # Ciclo de vida REST y estados del ticket
│   ├── database.py         # ORM SQLAlchemy y conexiones (PostgreSQL / SQLite)
│   ├── models.py           # Modelos relacionales de base de datos
│   ├── schemas.py          # Validación de datos y contratos Pydantic
│   └── services.py         # Motor Gemini REST Cascade y servicio Resend API
├── templates/
│   └── index.html          # SPA responsiva en Tailwind CSS, JavaScript y Lucide Icons
├── main.py                 # Servidor ASGI FastAPI, middleware y estáticos
├── render.yaml             # Blueprint de despliegue en Render Cloud
├── requirements.txt        # Dependencias de producción
└── README.md               # Documentación oficial del proyecto
```

---

### ⚡ Funcionalidades Clave

1. **Triaje Inteligente en Ruta (Google Gemini REST Cascade)**:
   * Análisis del problema del cliente mediante llamadas REST directas al API v1beta de Google Gemini.
   * **Reintento en Cascada (Cascade Fallback)**: Resiliencia garantizada mediante conmutación automática entre modelos (`gemini-1.5-flash` -> `gemini-2.0-flash` -> `gemini-1.5-pro` -> Motor de Reglas Local).
   * Determinación automática de Categoría (`MECÁNICA`, `ELÉCTRICA`, `HABITABILIDAD`, `OTROS`), Urgencia (`ALTA`, `MEDIA`, `BAJA`) y **Compromiso SLA (24h, 48h, 72h)**.

2. **Gobernanza y Service Desk de Flota (Vista Admin)**:
   * Acceso protegido por autenticación (`admin123`).
   * Evaluación, aprobación o rechazo justificado de las incidencias categorizadas por la IA.
   * Trazabilidad completa e historial de auditoría de cada vehículo.

3. **Panel Técnico e Integración SAP MM (Vista Tech)**:
   * Acceso restringido para el equipo de taller (`tech123`).
   * Emisión de Solicitudes de Pedido de recambios (**SolPed SAP**).
   * Registro del movimiento **MIGO 101** (Entrada de Mercancías) para el cierre de reparaciones.

4. **Notificaciones Transaccionales en Tiempo Real**:
   * Envío de correos formateados en HTML a través de **Resend API por puerto 443 (HTTPS)**, evitando bloqueos de red SMTP estándar en entornos de nube.

---

### 🛠️ Stack Tecnológico

| Capa / Módulo | Tecnología Utilizada |
| :--- | :--- |
| **Backend Framework** | Python 3.11 / FastAPI |
| **Persistencia de Datos** | PostgreSQL (Render Cloud) / SQLAlchemy ORM |
| **Motor de Inteligencia Artificial** | Google Gemini REST API (Cascade Fallback) |
| **Servicio de Notificaciones** | Resend REST API (HTTPS) |
| **Frontend UI** | HTML5 / Tailwind CSS / Lucide Icons / Vanilla JS |
| **Infraestructura & DevOps** | Render Web Services / Git / GitHub |

---

### 🔐 Credenciales de Acceso para Evaluación

| Perfil de Usuario | Pestaña de la Interfaz | Credencial / Contraseña |
| :--- | :--- | :--- |
| **Cliente / Usuario** | Notificar Incidencia | *Acceso Libre* |
| **Gobernanza Flota** | Gobernanza Flota | `admin123` |
| **Taller / Técnico** | Técnico & SAP MM | `tech123` |

---

### 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/stella-triage-engine.git
   cd stella-triage-engine
   ```

2. **Activar el entorno virtual**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el servidor local**:
   ```bash
   uvicorn main:app --reload
   ```
   *Acceder localmente en `http://127.0.0.1:8000`*

---

<a id="en"></a>
## 🇬🇧 English Version

**Stella Triage Engine** is an enterprise-grade software platform engineered for automated incident triage, artificial intelligence analysis, and operational fleet governance for the eco-friendly **Stella Smart Camper** van fleet.

The system seamlessly connects customer roadside assistance with fleet auditing workflows and spare parts management simulating the **SAP MM (Materials Management)** ecosystem.

---

### 🌐 Cloud Deployment (Production)

The platform is fully deployed and operational on **Render Cloud Infrastructure**:

* 🔗 **Live Application URL**: `https://stella-triage-engine.onrender.com`
* 🗄️ **Persistent Database**: PostgreSQL Cloud Managed Instance
* ✉️ **Notification Service**: Resend HTTPS REST API (Port 443)

---

### 🏗️ Architecture & Project Structure

```text
stella-triage-engine/
├── app/
│   ├── routers/
│   │   ├── auth.py         # Role-based authentication and access control
│   │   └── tickets.py      # Ticket lifecycle REST routes and states
│   ├── database.py         # SQLAlchemy ORM and connections (PostgreSQL / SQLite)
│   ├── models.py           # Database relational entity models
│   ├── schemas.py          # Data validation and Pydantic schemas
│   └── services.py         # Gemini REST Cascade Engine and Resend Email Service
├── templates/
│   └── index.html          # Responsive SPA built with Tailwind CSS & Lucide Icons
├── main.py                 # FastAPI ASGI server, middleware and static routes
├── render.yaml             # Render Cloud deployment blueprint
├── requirements.txt        # Production dependencies
└── README.md               # Official project documentation
```

---

### ⚡ Key Features

1. **Intelligent Roadside Triage (Google Gemini REST Cascade)**:
   * Analyzes customer reports using direct REST calls to Google Gemini v1beta API.
   * **Cascade Fallback Mechanism**: Guaranteed uptime via automated fallback between models (`gemini-1.5-flash` -> `gemini-2.0-flash` -> `gemini-1.5-pro` -> Local Rule Engine).
   * Automatic assignment of Category (`MECHANICAL`, `ELECTRICAL`, `HABITABILITY`, `OTHERS`), Urgency (`HIGH`, `MEDIUM`, `LOW`), and **SLA Commitments (24h, 48h, 72h)**.

2. **Fleet Governance & Service Desk (Admin View)**:
   * Password-protected access (`admin123`).
   * Review, approval, or justified rejection of AI-classified incidents.
   * Full traceability and historical audit log per vehicle.

3. **Technical Panel & SAP MM Integration (Tech View)**:
   * Restricted access for workshop staff (`tech123`).
   * Generation of spare parts Purchase Requisitions (**SAP SolPed**).
   * Registration of **MIGO 101** Goods Receipt movement to complete repairs.

4. **Real-Time Transactional Notifications**:
   * HTML-formatted email delivery using **Resend API over Port 443 (HTTPS)**, bypassing traditional cloud SMTP port blocks.

---

### 🛠️ Tech Stack

| Layer / Module | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.11 / FastAPI |
| **Data Persistence** | PostgreSQL (Render Cloud) / SQLAlchemy ORM |
| **Artificial Intelligence Engine** | Google Gemini REST API (Cascade Fallback) |
| **Notification Service** | Resend REST API (HTTPS) |
| **Frontend UI** | HTML5 / Tailwind CSS / Lucide Icons / Vanilla JS |
| **Infrastructure & DevOps** | Render Web Services / Git / GitHub |

---

### 🔐 Evaluation Credentials

| User Profile | Application Tab | Password Credential |
| :--- | :--- | :--- |
| **Customer / User** | Notificar Incidencia | *Public Access* |
| **Fleet Governance** | Gobernanza Flota | `admin123` |
| **Workshop / Tech** | Técnico & SAP MM | `tech123` |

---

### 🚀 Local Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tu-usuario/stella-triage-engine.git
   cd stella-triage-engine
   ```

2. **Activate virtual environment**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run local server**:
   ```bash
   uvicorn main:app --reload
   ```
   *Access locally at `http://127.0.0.1:8000`*