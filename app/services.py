import os
import json
import requests

# Claves de API desde variables de entorno de Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")


def classify_query(query_text: str) -> dict:
    """Clasificación con llamada REST directa y fallback en cascada de modelos Gemini."""
    if not GEMINI_API_KEY:
        return get_fallback_triage(query_text)

    # Reintento en cascada sobre modelos oficialmente soportados
    candidate_models = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
    
    prompt = f"""
    Eres el motor de triaje inteligente para la flota Stella Smart Camper.
    Analiza el siguiente problema reportado por el cliente: "{query_text}"

    Responde ÚNICAMENTE en formato JSON plano sin bloques de código markdown:
    {{
        "category": "MECÁNICA",
        "urgency": "ALTA",
        "department": "TALLER_MECANICO",
        "summary": "Resumen conciso en 1 frase",
        "estimated_sla": "24h"
    }}
    Categorías permitidas: MECÁNICA, ELÉCTRICA, HABITABILIDAD, OTROS.
    Urgencias permitidas: ALTA, MEDIA, BAJA.
    Departamentos: TALLER_MECANICO, ELECTRO_SISTEMAS, SOPORTE_GENERAL.
    SLAs: 24h, 48h, 72h.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    for model in candidate_models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            response = requests.post(url, json=payload, headers=headers, timeout=6)
            
            if response.status_code == 200:
                res_data = response.json()
                raw_text = res_data['candidates'][0]['content']['parts'][0]['text']
                clean_json = raw_text.replace("```json", "").replace("```", "").strip()
                print(f"[GEMINI SUCCESS] Triaje procesado con éxito mediante modelo: {model}")
                return json.loads(clean_json)
            else:
                print(f"[GEMINI WARN] Modelo {model} devolvió status {response.status_code}. Probando siguiente...")
        except Exception as e:
            print(f"[GEMINI ERROR] Fallo al consultar modelo {model}: {e}. Probando siguiente...")

    # Fallback automático local si fallan todos los endpoints externos
    print("[GEMINI FALLBACK] Aplicando motor de reglas local.")
    return get_fallback_triage(query_text)


def get_fallback_triage(query_text: str) -> dict:
    """Reglas de triaje locales por defecto cuando no hay respuesta del modelo."""
    text_lower = query_text.lower()
    if any(w in text_lower for w in ["batería", "bateria", "luces", "panel", "freno", "motor", "fusible"]):
        is_elec = any(w in text_lower for w in ["batería", "bateria", "luces", "panel", "fusible"])
        return {
            "category": "ELÉCTRICA" if is_elec else "MECÁNICA",
            "urgency": "ALTA",
            "department": "ELECTRO_SISTEMAS" if is_elec else "TALLER_MECANICO",
            "summary": "Incidencia crítica en subsistemas principales detectada.",
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
    """Envío real por Resend API (puerto 443) redirigido a tu correo para la demostración en vídeo."""
    if not RESEND_API_KEY:
        print(f"[EMAIL SIMULATED] Para: {to_email} | Asunto: {subject}")
        return

    # Redirección para garantizar entrega real en tu bandeja de entrada durante la demo
    demo_recipient = "garciaguadalupevanessa@outlook.es"

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": "Stella Smart Camper <onboarding@resend.dev>",
        "to": [demo_recipient],
        "subject": f"[Stella Support] {subject} (Destinatario: {to_email})",
        "html": f"<p><strong>[Aviso de Notificación enviado a: {to_email}]</strong></p><hr>" + body_html
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code in [200, 201]:
            print(f"[EMAIL DELIVERED] Correo entregado en bandeja real {demo_recipient} vía Resend API")
        else:
            print(f"[EMAIL API WARN] Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[EMAIL ERROR] Fallo en la API de correo: {e}")