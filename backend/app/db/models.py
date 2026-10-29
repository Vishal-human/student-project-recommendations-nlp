from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="student")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime(timezone=True), nullable=True)


class ProjectProposal(Base):
    """A student's submitted project proposal.

    Status lifecycle: pending -> approved | rejected
    Only ONE proposal per student can be approved.
    When a proposal is approved, its title is treated as "taken" by the NLP pipeline —
    future recommendations filter out semantically similar topics.
    """
    __tablename__ = "project_proposals"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=True)           # optional description
    interest_desc = Column(Text, nullable=True)      # what the student typed in the form
    stack_tags = Column(String, nullable=True)       # JSON array serialized as string
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    # Status: "pending" | "approved" | "rejected"
    status = Column(String, nullable=False, default="pending", index=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewer_notes = Column(Text, nullable=True)


class CorpusProject(Base):
    """Archived historical project in the university corpus.

    Synced with data/sample_corpus.json. Stores uploaded capstones,
    preprocessed tags, and domains.
    """
    __tablename__ = "corpus_projects"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)
    department = Column(String, nullable=False)
    tech_stack_tags = Column(String, nullable=False)  # JSON string
    domain_tags = Column(String, nullable=False)      # JSON string
    source = Column(String, default="upload")         # "seed" | "upload"
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
