# Stella Triage Engine 🚗⚡

**[ES]** Motor de triaje, clasificación y resumen asistido por Inteligencia Artificial para el ecosistema Stella. Desarrollado con **FastAPI** y **Pydantic**, este servicio procesa solicitudes de entrada, evalúa niveles de urgencia, asigna departamentos operativos y genera resúmenes concisos para optimizar el enrutamiento.

**[EN]** AI-powered triage, classification, and summarization engine built for the Stella ecosystem. Developed with **FastAPI** and **Pydantic**, this backend service processes incoming requests, evaluates urgency levels, assigns operational departments, and generates concise summaries to streamline workflow routing.

---

## 🚀 Features / Características

- **[ES]** Clasificación automática de peticiones en tiempo real.
- **[ES]** Evaluación estricta de datos de entrada mediante esquemas Pydantic.
- **[ES]** Asignación de urgencia y departamento responsable.
- **[EN]** Real-time automated query classification.
- **[EN]** Strict payload validation via Pydantic schemas.
- **[EN]** Automated urgency scoring and target department assignment.

---

## 🛠️ Tech Stack / Tecnologías

* **Language / Lenguaje:** Python 3.11+
* **Framework:** FastAPI
* **Data Validation / Validación:** Pydantic
* **Frontend UI (Testing):** Streamlit
* **Testing:** Pytest

---

## ⚙️ Quickstart / Inicio Rápido

```bash
# Clone the repository / Clonar el repositorio
git clone [https://github.com/garciaguadalupevanessa-bit/stella-triage-engine.git](https://github.com/garciaguadalupevanessa-bit/stella-triage-engine.git)

# Create and activate virtual environment / Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# Install dependencies / Instalar dependencias
pip install -r requirements.txt

# Run FastAPI server / Ejecutar servidor FastAPI
uvicorn main:app --reload