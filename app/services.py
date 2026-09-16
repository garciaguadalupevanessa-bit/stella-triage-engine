import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

# --- Servicio de Triaje Gemini IA ---

def classify_query(query: str) -> dict:
    prompt = f"""
    Eres el motor de triaje inteligente de Stella Triage Engine para una flota de vans camperizadas ecológicas.
    Analiza la incidencia enviada por el cliente y clasifícala devolviendo ÚNICAMENTE un objeto JSON válido con la siguiente estructura:
    {{
      "category": "Categoría técnica (Ej: Peligro Mecánico, Climatización, Batería/Energía, Domótica/Software, Agua/Gas, Carrocería)",
      "urgency": "HIGH / ALTA, MEDIUM / MEDIA o LOW / BAJA",
      "department": "Departamento asignado (Ej: Asistencia en Carretera, Soporte Técnico, Mantenimiento Flota, Almacén Recambios)",
      "summary": "Resumen técnico sintético del problema en máximo 20 palabras"
    }}

    Incidencia enviada por el cliente: "{query}"
    """

    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    triage_result = {
        "category": "Consulta General / Domótica",
        "urgency": "MEDIUM / MEDIA",
        "department": "Soporte Técnico Flota",
        "summary": f"Motor Base Triage: {query[:40]}...",
        "estimated_sla": "24 a 48 Horas"
    }

    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)  # type: ignore
            model = genai.GenerativeModel("gemini-1.5-flash")  # type: ignore
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            triage_result["category"] = data.get("category", triage_result["category"])
            triage_result["urgency"] = data.get("urgency", triage_result["urgency"])
            triage_result["department"] = data.get("department", triage_result["department"])
            triage_result["summary"] = data.get("summary", triage_result["summary"])
        except Exception as e:
            print(f"Error procesando Gemini API: {e}")

    # Lógica de SLA
    urgency_upper = str(triage_result["urgency"]).upper()
    if "HIGH" in urgency_upper or "ALTA" in urgency_upper:
        triage_result["estimated_sla"] = "Atención Prioritaria (< 4 Horas)"
    elif "LOW" in urgency_upper or "BAJA" in urgency_upper:
        triage_result["estimated_sla"] = "3 a 5 Días Laborables"
    else:
        triage_result["estimated_sla"] = "24 a 48 Horas"

    return triage_result

# --- Servicio de Envíos de Correo Transaccional ---

def send_status_email(to_email: str, subject: str, html_content: str):
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASSWORD", "")

    if not smtp_user or not smtp_pass:
        print(f"[EMAIL SIMULATED] Para: {to_email} | Asunto: {subject}")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = f"Stella Smart Camper <{smtp_user}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"[EMAIL SENT] Notificación enviada a {to_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] Error enviando correo: {e}")