from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.deps import require_role
from app.schemas.auth import UserOut

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard/student")
def student_dashboard(current_user: User = Depends(require_role("student"))):
    return {
        "message": f"Welcome, {current_user.name}!",
        "role": current_user.role,
        "next_step": "Browse recommended project topics (Stage 2 feature).",
    }


@router.get("/dashboard/teacher")
def teacher_dashboard(
    current_user: User = Depends(require_role("teacher")),
    db: Session = Depends(get_db),
):
    student_count = db.query(User).filter(User.role == "student").count()
    return {
        "message": f"Welcome, {current_user.name}!",
        "role": current_user.role,
        "registered_students": student_count,
    }


@router.get("/teacher/students", response_model=list[UserOut])
def list_students(
    current_user: User = Depends(require_role("teacher")),
    db: Session = Depends(get_db),
):
    return db.query(User).filter(User.role == "student").order_by(User.created_at.desc()).all()
