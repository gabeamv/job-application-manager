from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional
import uuid
from datetime import datetime, date
from zoneinfo import ZoneInfo

class Base(DeclarativeBase):
    pass

class Companies(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(types.Text, unique=True, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(types.Text)
    industry: Mapped[Optional[str]] = mapped_column(types.Text)

    job_postings: Mapped[list["JobPostings"]] = relationship(back_populates="company", passive_deletes=True)

class JobPostings(Base):
    __tablename__ = "job_postings"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    job_title: Mapped[str] = mapped_column(types.Text, nullable=False)
    url: Mapped[str] = mapped_column(types.Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(types.Text)
    employment_type: Mapped[Optional[str]] = mapped_column(types.Text)
    salary_min: Mapped[Optional[float]] = mapped_column(types.Numeric(8, 2))
    salary_max: Mapped[Optional[float]] = mapped_column(types.Numeric(8,2))
    deadline: Mapped[Optional[date]] = mapped_column(types.Date)
    date_posted: Mapped[Optional[date]] = mapped_column(types.Date)

    company: Mapped["Companies"] = relationship(back_populates="job_postings")
    applications: Mapped[list["Applications"]] = relationship(back_populates="job_posting", passive_deletes=True)
    cover_letters: Mapped[list["CoverLetters"]] = relationship(back_populates="job_posting", passive_deletes=True)
    job_postings_skills: Mapped[list["JobPostingsSkills"]] = relationship(back_populates="job_posting", passive_deletes=True)

class Resumes(Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(types.Text, nullable=False)
    version: Mapped[float] = mapped_column(types.Numeric(6, 2), nullable=False)
    url: Mapped[str] = mapped_column(types.Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "version", name="uq_resumes_name_version"),
    )

    applications: Mapped[list["Applications"]] = relationship(back_populates="resume", passive_deletes=True)

class CoverLetters(Base):
    __tablename__ = "cover_letters"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    job_postings_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(types.Text, nullable=False)
    url: Mapped[str] = mapped_column(types.Text, nullable=False)

    job_posting: Mapped["JobPostings"] = relationship(back_populates="cover_letters")

class Applications(Base):
    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    job_postings_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    resumes_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    date_applied: Mapped[date] = mapped_column(types.Date, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(types.Text, default="pending")
    created_at: Mapped[Optional[datetime]] = mapped_column(types.TIMESTAMP(timezone=True), default=lambda: datetime.now(ZoneInfo("America/Los_Angeles")))
    updated_at: Mapped[Optional[datetime]] = mapped_column(types.TIMESTAMP(timezone=True))

    job_posting: Mapped["JobPostings"] = relationship(back_populates="applications")
    resume: Mapped["Resumes"] = relationship(back_populates="applications")
    interviews: Mapped[list["Interviews"]] = relationship(back_populates="application", passive_deletes=True)

class Interviews(Base):
    __tablename__ = "interviews"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    applications_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(types.Text)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(types.TIMESTAMP(timezone=True))
    notes: Mapped[Optional[str]] = mapped_column(types.Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(types.TIMESTAMP(timezone=True), default=lambda: datetime.now(datetime.UTC))

    application: Mapped["Applications"] = relationship(back_populates="interviews")

class Skills(Base):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(types.Text, unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(types.Text)

    job_postings_skills: Mapped[list["JobPostingsSkills"]] = relationship(back_populates="skill", passive_deletes=True)
    
class JobPostingsSkills(Base):
    __tablename__ = "job_postings_skills"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    job_postings_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    skills_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("job_postings_id", "skills_id", name="uq_job_postings_job_postings_id_skills_id"),
    )

    skill: Mapped["Skills"] = relationship(back_populates="job_postings_skills")
    job_posting: Mapped["JobPostings"] = relationship(back_populates="job_postings_skills")