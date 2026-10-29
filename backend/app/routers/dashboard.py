from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import ProjectProposal, User
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


@router.get("/dashboard/supervisor")
def supervisor_dashboard(
    current_user: User = Depends(require_role("supervisor")),
    db: Session = Depends(get_db),
):
    """Institution-level overview: read-only counts across all users and proposals."""
    count = lambda status: db.query(ProjectProposal).filter(ProjectProposal.status == status).count()
    return {
        "message": f"Welcome, {current_user.name}!",
        "role": current_user.role,
        "students": db.query(User).filter(User.role == "student").count(),
        "teachers": db.query(User).filter(User.role == "teacher").count(),
        "proposals": {
            "total": db.query(ProjectProposal).count(),
            "pending": count("pending"),
            "approved": count("approved"),
            "rejected": count("rejected"),
        },
    }


@router.get("/teacher/students", response_model=list[UserOut])
def list_students(
    current_user: User = Depends(require_role("teacher")),
    db: Session = Depends(get_db),
):
    return db.query(User).filter(User.role == "student").order_by(User.created_at.desc()).all()
