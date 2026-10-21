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


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(topics.router)
app.include_router(supervisor.router)
app.include_router(proposals.router)
