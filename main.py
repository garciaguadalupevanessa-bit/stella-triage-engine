import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.database import engine, Base
from app.routers import auth, tickets

# Inicializar tablas en la Base de Datos (PostgreSQL/SQLite)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stella Triage Engine",
    description="AI-powered triage for Smart Eco Camper Vans, lifecycle management, and SAP MM integration",
    version="1.0.0"
)

# Garantizar y resolver la ruta absoluta de la carpeta static
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar Routers de la aplicación
app.include_router(auth.router)
app.include_router(tickets.router)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

class LoginRequest(BaseModel):
    password: str

@app.post("/auth/login")
def login(data: LoginRequest):
    if data.password == "admin123":
        return {"role": "admin", "token": "session_admin"}
    elif data.password == "tech123":
        return {"role": "tech", "token": "session_tech"}
    else:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")