"""Creates the DB tables and the default teacher + supervisor accounts if they don't exist yet.

Run once after the database is up: `docker compose exec backend python -m app.seed`
"""

from app.core.config import (
    SUPERVISOR_EMAIL, SUPERVISOR_NAME, SUPERVISOR_PASSWORD,
    TEACHER_EMAIL, TEACHER_NAME, TEACHER_PASSWORD,
)
from app.core.security import hash_password
from app.db.database import Base, SessionLocal, engine
from app.db.models import User


def run():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        for role, name, email, password in (
            ("teacher", TEACHER_NAME, TEACHER_EMAIL, TEACHER_PASSWORD),
            ("supervisor", SUPERVISOR_NAME, SUPERVISOR_EMAIL, SUPERVISOR_PASSWORD),
        ):
            if db.query(User).filter(User.email == email).first():
                print(f"{role.capitalize()} account already exists: {email}")
                continue
            db.add(User(name=name, email=email, password_hash=hash_password(password), role=role))
            db.commit()
            print(f"Created {role} account: {email} / {password}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
