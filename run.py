from fastapi import FastAPI
from api import (applications, companies, cover_letters, interviews, job_postings,
job_postings_skills, resumes, skills, test)

app = FastAPI()

app.include_router(test.router, prefix="/api/test", tags=["test"])
app.include_router(applications.router, prefix="/api/applications", tags=["applications"])
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(cover_letters.router, prefix="/api/cover_letters", tags=["cover_letters"])
app.include_router(interviews.router, prefix="/api/interviews", tags=["interviews"])
app.include_router(job_postings.router, prefix="/api/jobs_postings", tags=["job_postings"])
app.include_router(job_postings_skills.router, prefix="/api/job_postings_skills", tags=["job_postings_skills"])
app.include_router(resumes.router, prefix="/api/resumes", tags=["resumes"])
app.include_router(skills.router, prefix="/api/skills", tags=["skills"])
