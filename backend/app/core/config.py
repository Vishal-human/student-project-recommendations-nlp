import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://nlp_user:nlp_password@postgres:5432/nlp_project",
)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))

TEACHER_EMAIL = os.getenv("TEACHER_EMAIL", "teacher@college.edu")
TEACHER_PASSWORD = os.getenv("TEACHER_PASSWORD", "teacher123")
TEACHER_NAME = os.getenv("TEACHER_NAME", "Default Teacher")
