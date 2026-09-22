# Entity-Relationship Diagram

Generated from [models/models.py](../models/models.py).

```mermaid
erDiagram
    COMPANIES ||--o{ JOB_POSTINGS : posts
    JOB_POSTINGS ||--o{ COVER_LETTERS : has
    JOB_POSTINGS ||--o{ APPLICATIONS : has
    JOB_POSTINGS ||--o{ JOB_POSTINGS_SKILLS : requires
    RESUMES ||--o{ APPLICATIONS : used_in
    APPLICATIONS ||--o{ INTERVIEWS : has
    SKILLS ||--o{ JOB_POSTINGS_SKILLS : linked_to

    COMPANIES {
        uuid id PK
        text name UK
        text url
        text industry
    }

    JOB_POSTINGS {
        uuid id PK
        uuid company_id FK
        text job_title
        text url
        text description
        text employment_type
        numeric salary_min
        numeric salary_max
        date deadline
        date date_posted
    }

    RESUMES {
        uuid id PK
        text name UK
        numeric version UK
        text url
    }

    COVER_LETTERS {
        uuid id PK
        uuid job_postings_id FK
        text name
        text url
    }

    APPLICATIONS {
        uuid id PK
        uuid job_postings_id FK
        uuid resumes_id FK
        date date_applied
        text status
        timestamptz created_at
        timestamptz updated_at
    }

    INTERVIEWS {
        uuid id PK
        uuid applications_id FK
        text type
        timestamptz scheduled_at
        text notes
        timestamptz created_at
    }

    SKILLS {
        uuid id PK
        text name UK
        text description
    }

    JOB_POSTINGS_SKILLS {
        uuid id PK
        uuid job_postings_id FK
        uuid skills_id FK
    }
```
