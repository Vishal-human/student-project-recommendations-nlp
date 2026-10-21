"""
Proposals router — the core workflow for real university use.

Student endpoints:
  POST /proposals/submit      - submit a proposal (one active proposal per student)
  GET  /proposals/mine        - see own proposals + status

Teacher endpoints:
  GET  /proposals/pending     - all pending proposals, auto-formatted for duplicate checking
  POST /proposals/{id}/approve - approve (first-submitted wins on duplicates)
  POST /proposals/{id}/reject  - reject with optional notes

Public (pipeline):
  GET  /proposals/approved-titles - list of approved titles for recommendation filtering
"""
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import ProjectProposal, User
from app.deps import get_current_user, require_role

router = APIRouter(prefix="/proposals", tags=["proposals"])


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class SubmitProposalRequest(BaseModel):
    title: str
    abstract: str = ""
    interest_desc: str = ""
    stack_tags: list[str] = []


class ProposalOut(BaseModel):
    id: int
    title: str
    abstract: str | None
    status: str
    submitted_at: str
    reviewed_at: str | None
    reviewer_notes: str | None
    student_name: str | None = None
    student_email: str | None = None
    roll_no: str | None = None   # derived from email prefix for display


class ReviewRequest(BaseModel):
    notes: str = ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fmt_dt(dt) -> str | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def _proposal_to_out(p: ProjectProposal, db: Session, include_student: bool = False) -> ProposalOut:
    student = db.query(User).filter(User.id == p.student_id).first() if include_student else None
    roll_no = student.email.split("@")[0].upper() if student else None
    return ProposalOut(
        id=p.id,
        title=p.title,
        abstract=p.abstract or "",
        status=p.status,
        submitted_at=_fmt_dt(p.submitted_at),
        reviewed_at=_fmt_dt(p.reviewed_at),
        reviewer_notes=p.reviewer_notes,
        student_name=student.name if student else None,
        student_email=student.email if student else None,
        roll_no=roll_no,
    )


# ---------------------------------------------------------------------------
# Student endpoints
# ---------------------------------------------------------------------------

@router.post("/submit", response_model=ProposalOut)
def submit_proposal(
    body: SubmitProposalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a project proposal.

    Rules:
    - A student can only have one pending or approved proposal at a time.
    - If they have a pending one, submitting again updates it (they can refine).
    - If one is already approved, they cannot submit a new one.
    """
    if not body.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty.")

    # Block if already approved
    existing_approved = (
        db.query(ProjectProposal)
        .filter(ProjectProposal.student_id == current_user.id, ProjectProposal.status == "approved")
        .first()
    )
    if existing_approved:
        raise HTTPException(
            status_code=400,
            detail="You already have an approved project. Contact your supervisor to make changes."
        )

    # Update pending if exists, else create new
    existing_pending = (
        db.query(ProjectProposal)
        .filter(ProjectProposal.student_id == current_user.id, ProjectProposal.status == "pending")
        .first()
    )
    if existing_pending:
        existing_pending.title = body.title.strip()
        existing_pending.abstract = body.abstract.strip()
        existing_pending.interest_desc = body.interest_desc.strip()
        existing_pending.stack_tags = json.dumps(body.stack_tags)
        existing_pending.submitted_at = datetime.now(timezone.utc)  # reset timestamp on update
        db.commit()
        db.refresh(existing_pending)
        return _proposal_to_out(existing_pending, db)

    proposal = ProjectProposal(
        student_id=current_user.id,
        title=body.title.strip(),
        abstract=body.abstract.strip(),
        interest_desc=body.interest_desc.strip(),
        stack_tags=json.dumps(body.stack_tags),
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return _proposal_to_out(proposal, db)


@router.get("/mine", response_model=list[ProposalOut])
def get_my_proposals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Student: see all their proposals with current status."""
    proposals = (
        db.query(ProjectProposal)
        .filter(ProjectProposal.student_id == current_user.id)
        .order_by(ProjectProposal.submitted_at.desc())
        .all()
    )
    return [_proposal_to_out(p, db) for p in proposals]


# ---------------------------------------------------------------------------
# Teacher endpoints
# ---------------------------------------------------------------------------

@router.get("/pending", response_model=list[ProposalOut])
def get_pending_proposals(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("teacher")),
):
    """Teacher: all pending proposals, sorted by submission time (oldest first = priority)."""
    proposals = (
        db.query(ProjectProposal)
        .filter(ProjectProposal.status == "pending")
        .order_by(ProjectProposal.submitted_at.asc())  # oldest = priority
        .all()
    )
    return [_proposal_to_out(p, db, include_student=True) for p in proposals]


@router.get("/all", response_model=list[ProposalOut])
def get_all_proposals(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("teacher")),
):
    """Teacher: all proposals (all statuses), sorted by time."""
    proposals = (
        db.query(ProjectProposal)
        .order_by(ProjectProposal.submitted_at.asc())
        .all()
    )
    return [_proposal_to_out(p, db, include_student=True) for p in proposals]


@router.post("/{proposal_id}/approve", response_model=ProposalOut)
def approve_proposal(
    proposal_id: int,
    body: ReviewRequest = ReviewRequest(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("teacher")),
):
    """Approve a proposal.

    The student's other pending proposals are auto-rejected.
    Timestamp matters: if a semantically similar proposal was submitted EARLIER by
    another student, this endpoint allows the teacher to approve it — the UI will
    show the earlier submission first so teachers naturally approve in priority order.
    """
    proposal = db.query(ProjectProposal).filter(ProjectProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found.")
    if proposal.status != "pending":
        raise HTTPException(status_code=400, detail=f"Proposal is already {proposal.status}.")

    now = datetime.now(timezone.utc)
    proposal.status = "approved"
    proposal.reviewed_at = now
    proposal.reviewer_id = current_user.id
    proposal.reviewer_notes = body.notes

    # Auto-reject any other pending proposals from the same student
    other_pending = (
        db.query(ProjectProposal)
        .filter(
            ProjectProposal.student_id == proposal.student_id,
            ProjectProposal.id != proposal_id,
            ProjectProposal.status == "pending",
        )
        .all()
    )
    for op in other_pending:
        op.status = "rejected"
        op.reviewed_at = now
        op.reviewer_notes = "Auto-rejected: another proposal was approved."

    db.commit()
    db.refresh(proposal)
    return _proposal_to_out(proposal, db, include_student=True)


@router.post("/{proposal_id}/reject", response_model=ProposalOut)
def reject_proposal(
    proposal_id: int,
    body: ReviewRequest = ReviewRequest(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("teacher")),
):
    """Reject a proposal. Student can resubmit with a revised topic."""
    proposal = db.query(ProjectProposal).filter(ProjectProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found.")
    if proposal.status != "pending":
        raise HTTPException(status_code=400, detail=f"Proposal is already {proposal.status}.")

    proposal.status = "rejected"
    proposal.reviewed_at = datetime.now(timezone.utc)
    proposal.reviewer_id = current_user.id
    proposal.reviewer_notes = body.notes
    db.commit()
    db.refresh(proposal)
    return _proposal_to_out(proposal, db, include_student=True)


# ---------------------------------------------------------------------------
# Pipeline endpoint — used by recommendation engine to filter taken topics
# ---------------------------------------------------------------------------

@router.get("/approved-titles")
def get_approved_titles(
    db: Session = Depends(get_db),
):
    """Returns list of approved project titles — used to filter recommendations.
    Public: no auth needed, called internally by the NLP pipeline.
    """
    approved = (
        db.query(ProjectProposal.title)
        .filter(ProjectProposal.status == "approved")
        .all()
    )
    return {"titles": [r.title for r in approved]}
