import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

# Configuración de Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    configure_fn = getattr(genai, "configure", None)
    if callable(configure_fn):
        configure_fn(api_key=GEMINI_API_KEY)

def classify_query(query_text: str) -> dict:
    """Clasifica la consulta con Gemini API o aplica el fallback de reglas locales."""
    if not GEMINI_API_KEY:
        return get_fallback_triage(query_text)

    try:
        model_cls = getattr(genai, "GenerativeModel", None)
        if not model_cls:
            return get_fallback_triage(query_text)

        # Nombre de modelo estable y compatible con v1beta
        model = model_cls("gemini-1.5-flash-latest")
        prompt = f"""
        Eres el motor de triaje inteligente para la flota Stella Smart Camper.
        Analiza el siguiente problema reportado por el cliente: "{query_text}"

        Responde ÚNICAMENTE en formato JSON plano con esta estructura:
        {{
            "category": "MECÁNICA" | "ELÉCTRICA" | "HABITABILIDAD" | "OTROS",
            "urgency": "ALTA" | "MEDIA" | "BAJA",
            "department": "TALLER_MECANICO" | "ELECTRO_SISTEMAS" | "SOPORTE_GENERAL",
            "summary": "Resumen conciso en 1 frase",
            "estimated_sla": "24h" | "48h" | "72h"
        }}
        """
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"[GEMINI API ERROR] {e}. Aplicando fallback de triaje.")
        return get_fallback_triage(query_text)

def get_fallback_triage(query_text: str) -> dict:
    """Reglas de triaje locales por defecto."""
    text_lower = query_text.lower()
    if any(w in text_lower for w in ["batería", "bateria", "luces", "panel", "freno", "motor"]):
        return {
            "category": "ELÉCTRICA" if "batería" in text_lower or "luces" in text_lower else "MECÁNICA",
            "urgency": "ALTA",
            "department": "ELECTRO_SISTEMAS" if "batería" in text_lower else "TALLER_MECANICO",
            "summary": "Incidencia crítica en sistemas principales detectada.",
            "estimated_sla": "24h"
        }
    return {
        "category": "HABITABILIDAD",
        "urgency": "MEDIA",
        "department": "SOPORTE_GENERAL",
        "summary": "Consulta de uso o equipamiento de la camper.",
        "estimated_sla": "48h"
    }

def send_status_email(to_email: str, subject: str, body_html: str):
    """Envía un correo con SSL o TLS según configuración."""
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 465))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_password = os.environ.get("SMTP_PASSWORD", "")

    if not smtp_user or not smtp_password:
        print(f"[EMAIL SIMULATED] Para: {to_email} | Asunto: {subject}")
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Stella Support <{smtp_user}>"
        msg["To"] = to_email
        msg.attach(MIMEText(body_html, "html"))

        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, to_email, msg.as_string())
        else:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, to_email, msg.as_string())

        print(f"[EMAIL SENT] Correo enviado exitosamente a {to_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] Error enviando correo: {e}")