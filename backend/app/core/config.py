import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./nlp_project.db",
)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))

TEACHER_EMAIL = os.getenv("TEACHER_EMAIL", "teacher@college.edu")
TEACHER_PASSWORD = os.getenv("TEACHER_PASSWORD", "teacher123")
TEACHER_NAME = os.getenv("TEACHER_NAME", "Default Teacher")

SUPERVISOR_EMAIL = os.getenv("SUPERVISOR_EMAIL", "supervisor@college.edu")
SUPERVISOR_PASSWORD = os.getenv("SUPERVISOR_PASSWORD", "supervisor123")
SUPERVISOR_NAME = os.getenv("SUPERVISOR_NAME", "Default Supervisor")
