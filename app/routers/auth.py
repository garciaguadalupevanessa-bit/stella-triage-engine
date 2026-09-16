import os
from fastapi import APIRouter, HTTPException, status
from app.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/api", tags=["Auth"])

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
TECH_PASSWORD = os.environ.get("TECH_PASSWORD", "tech123")

@router.post("/login", response_model=LoginResponse)
def login_role(payload: LoginRequest):
    if payload.role == "admin" and payload.password == ADMIN_PASSWORD:
        return LoginResponse(success=True, role="admin", message="Acceso concedido a Gobernanza Flota")
    elif payload.role == "tech" and payload.password == TECH_PASSWORD:
        return LoginResponse(success=True, role="tech", message="Acceso concedido a Técnico & SAP MM")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta para el rol seleccionado"
        )