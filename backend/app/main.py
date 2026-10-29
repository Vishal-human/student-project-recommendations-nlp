from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.db.database import Base, engine
from app.routers import auth, dashboard, topics, supervisor, proposals

app = FastAPI(title="TopicMatch — Student Project Recommendation Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    # No migration tool (Alembic) set up yet — this keeps `users` in sync with
    # model changes across restarts without wiping the DB volume every time.
    if engine.dialect.name == "postgresql":
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR"))
            conn.execute(
                text("ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMPTZ")
            )


@app.get("/")
def root():
    return {
        "app": "TopicMatch — Student Project Recommendation Platform API",
        "status": "running",
        "docs_url": "http://127.0.0.1:8000/docs",
        "redoc_url": "http://127.0.0.1:8000/redoc",
        "frontend_url": "http://localhost:5173",
        "message": "Visit /docs for the interactive Swagger API Explorer, or http://localhost:5173 for the React Web App."
    }


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(topics.router)
app.include_router(supervisor.router)
app.include_router(proposals.router)
