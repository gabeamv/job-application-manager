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

    job_postings: Mapped[list["JobPostings"]] = relationship(back_populates="company")

class JobPostings(Base):
    __tablename__ = "job_postings"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"))
    job_title: Mapped[str] = mapped_column(types.Text, nullable=False)
    url: Mapped[str] = mapped_column(types.Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(types.Text)
    employment_type: Mapped[Optional[str]] = mapped_column(types.Text)
    salary_min: Mapped[Optional[float]] = mapped_column(types.Numeric(8, 2))
    salary_max: Mapped[Optional[float]] = mapped_column(types.Numeric(8,2))
    deadline: Mapped[Optional[date]] = mapped_column(types.Date)
    date_posted: Mapped[Optional[date]] = mapped_column(types.Date)

    company: Mapped["Companies"] = relationship(back_populates="job_postings")
    applications: Mapped[list["Applications"]] = relationship(back_populates="job_posting")
    cover_letters: Mapped[list["CoverLetters"]] = relationship(back_populates="job_posting")
    job_postings_skills: Mapped[list["JobPostingsSkills"]] = relationship(back_populates="job_posting")

class Resumes(Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(types.Text, nullable=False)
    version: Mapped[float] = mapped_column(types.Numeric(6, 2), nullable=False)
    url: Mapped[str] = mapped_column(types.Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "version", name="uq_resumes_name_version"),
    )

    applications: Mapped[list["Applications"]] = relationship(back_populates="resume")

class CoverLetters(Base):
    __tablename__ = "cover_letters"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    job_postings_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id"), nullable=False)
    name: Mapped[str] = mapped_column(types.Text, nullable=False)
    url: Mapped[str] = mapped_column(types.Text, nullable=False)

    job_posting: Mapped["JobPostings"] = relationship(back_populates="cover_letters")

class Applications(Base):
    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    job_postings_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id"), nullable=False)
    resumes_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resumes.id"), nullable=False)
    date_applied: Mapped[date] = mapped_column(types.Date, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(types.Text, default="pending")
    created_at: Mapped[Optional[datetime]] = mapped_column(types.TIMESTAMP(timezone=True), default=lambda: datetime.now(ZoneInfo("America/Los_Angeles")))
    updated_at: Mapped[Optional[datetime]] = mapped_column(types.TIMESTAMP(timezone=True))

    job_posting: Mapped["JobPostings"] = relationship(back_populates="applications")
    resume: Mapped["Resumes"] = relationship(back_populates="applications")
    interviews: Mapped[list["Interviews"]] = relationship(back_populates="application")

class Interviews(Base):
    __tablename__ = "interviews"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    applications_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("applications.id"), nullable=False)
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

    job_postings_skills: Mapped[list["JobPostingsSkills"]] = relationship(back_populates="skill")
    
class JobPostingsSkills(Base):
    __tablename__ = "job_postings_skills"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    job_postings_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id"), nullable=False)
    skills_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id"), nullable=False)

    skill: Mapped["Skills"] = relationship(back_populates="job_postings_skills")
    job_posting: Mapped["JobPostings"] = relationship(back_populates="job_postings_skills")