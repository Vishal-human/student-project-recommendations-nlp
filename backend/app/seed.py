"""Creates the DB tables and the default teacher account if they don't exist yet.

Run once after the database is up: `docker compose exec backend python -m app.seed`
"""

from app.core.config import TEACHER_EMAIL, TEACHER_NAME, TEACHER_PASSWORD
from app.core.security import hash_password
from app.db.database import Base, SessionLocal, engine
from app.db.models import User


def run():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == TEACHER_EMAIL).first()
        if existing:
            print(f"Teacher account already exists: {TEACHER_EMAIL}")
            return

        teacher = User(
            name=TEACHER_NAME,
            email=TEACHER_EMAIL,
            password_hash=hash_password(TEACHER_PASSWORD),
            role="teacher",
        )
        db.add(teacher)
        db.commit()
        print(f"Created teacher account: {TEACHER_EMAIL} / {TEACHER_PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
