from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid
from datetime import datetime, date
from zoneinfo import ZoneInfo

class Base(DeclarativeBase):
    pass

class Companies(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(types.Text, unique=True, nullable=False)
    url: Mapped[str] = mapped_column(types.Text)
    industry: Mapped[str] = mapped_column(types.Text)

class JobPostings(Base):
    __tablename__ = "job_postings"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"))
    job_title: Mapped[str] = mapped_column(types.Text, nullable=False)
    url: Mapped[str] = mapped_column(types.Text, nullable=False)
    description: Mapped[str] = mapped_column(types.Text)
    employment_type: Mapped[str] = mapped_column(types.Text)
    salary_min: Mapped[float] = mapped_column(types.Numeric(8, 2))
    salary_max: Mapped[float] = mapped_column(types.Numeric(8,2))
    deadline: Mapped[date] = mapped_column(types.Date)
    date_posted: Mapped[date] = mapped_column(types.Date)

class Resumes(Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(types.Text, nullable=False)
    version: Mapped[int] = mapped_column(types.INTEGER, nullable=False)
    url: Mapped[str] = mapped_column(types.Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "version", name="uq_resumes_name_version"),
    )

class CoverLetters(Base):
    __tablename__ = "cover_letters"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    job_postings_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id"))
    name: Mapped[str] = mapped_column(types.Text, nullable=False)
    url: Mapped[str] = mapped_column(types.Text, nullable=False)

class Applications(Base):
    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    job_postings_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id"))
    resumes_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resumes.id"))
    date_applied: Mapped[date] = mapped_column(types.Date, nullable=False)
    status: Mapped[str] = mapped_column(types.Text, default="pending")
    created_at: Mapped[datetime] = mapped_column(types.TIMESTAMP(timezone=True), default=datetime.now(ZoneInfo("America/Los_Angeles")))
    updated_at: Mapped[datetime] = mapped_column(types.TIMESTAMP(timezone=True))

class Interviews(Base):
    __tablename__ = "interviews"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    applications_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("applications.id"))
    type: Mapped[str] = mapped_column(types.Text)
    scheduled_at: Mapped[datetime] = mapped_column(types.TIMESTAMP(timezone=True))
    notes: Mapped[str] = mapped_column(types.Text)
    created_at: Mapped[datetime] = mapped_column(types.TIMESTAMP(timezone=True), default=datetime.now(ZoneInfo("America/Los_Angeles")))

class Skills(Base):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(types.Text, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(types.Text)

class JobPostingsSkills(Base):
    __tablename__ = "job_postings_skills"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    job_postings_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id"))
    skills_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id"))