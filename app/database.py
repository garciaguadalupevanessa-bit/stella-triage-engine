import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import sessionmaker

# Obtener URL de PostgreSQL desde Render o usar SQLite por defecto
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./stella_triage.db")

# Ajustar prefijo si Render proporciona postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}    


engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        