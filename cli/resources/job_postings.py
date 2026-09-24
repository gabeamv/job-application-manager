from cli import prompts
from cli.http_client import ApiClient, ApiError
from cli.prompts import UNSET
from cli.serialize import to_payload

# NOTE: matches the "/api/jobs_postings" prefix registered in run.py.
RESOURCE_PATH = "/api/jobs_postings/"


def _print(job_posting: dict):
    print(f"  id:              {job_posting['id']}")
    print(f"  company_id:      {job_posting['company_id']}")
    print(f"  job_title:       {job_posting['job_title']}")
    print(f"  url:             {job_posting['url']}")
    print(f"  description:     {job_posting.get('description') or '-'}")
    print(f"  employment_type: {job_posting.get('employment_type') or '-'}")
    print(f"  salary_min:      {job_posting.get('salary_min') if job_posting.get('salary_min') is not None else '-'}")
    print(f"  salary_max:      {job_posting.get('salary_max') if job_posting.get('salary_max') is not None else '-'}")
    print(f"  deadline:        {job_posting.get('deadline') or '-'}")
    print(f"  date_posted:     {job_posting.get('date_posted') or '-'}")


def create(client: ApiClient):
    print("\n-- Create Job Posting --")
    payload = to_payload({
        "company_id": prompts.prompt_required_uuid("Company ID"),
        "job_title": prompts.prompt_required_str("Job title"),
        "url": prompts.prompt_required_str("URL"),
        "description": prompts.prompt_optional_str("Description"),
        "employment_type": prompts.prompt_optional_str("Employment type"),
        "salary_min": prompts.prompt_optional_float("Salary min"),
        "salary_max": prompts.prompt_optional_float("Salary max"),
        "deadline": prompts.prompt_optional_date("Deadline"),
        "date_posted": prompts.prompt_optional_date("Date posted"),
    })
    try:
        job_posting = client.post(RESOURCE_PATH, json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nJob posting created:")
    _print(job_posting)


def get_by_id(client: ApiClient):
    print("\n-- Get Job Posting by ID --")
    job_posting_id = prompts.prompt_required_uuid("Job posting ID")
    try:
        job_posting = client.get(f"{RESOURCE_PATH}{job_posting_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print()
    _print(job_posting)


def get_all(client: ApiClient):
    print("\n-- All Job Postings --")
    try:
        job_postings = client.get(RESOURCE_PATH)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    if not job_postings:
        print("No job postings found.")
        return
    for job_posting in job_postings:
        _print(job_posting)
        print()


def update(client: ApiClient):
    print("\n-- Update Job Posting --")
    job_posting_id = prompts.prompt_required_uuid("Job posting ID")

    fields = {
        "company_id": prompts.prompt_update_uuid("Company ID"),
        "job_title": prompts.prompt_update_str("Job title"),
        "url": prompts.prompt_update_str("URL"),
        "description": prompts.prompt_update_str("Description"),
        "employment_type": prompts.prompt_update_str("Employment type"),
        "salary_min": prompts.prompt_update_float("Salary min"),
        "salary_max": prompts.prompt_update_float("Salary max"),
        "deadline": prompts.prompt_update_date("Deadline"),
        "date_posted": prompts.prompt_update_date("Date posted"),
    }
    payload = to_payload({k: v for k, v in fields.items() if v is not UNSET})

    if not payload:
        print("No changes entered.")
        return
    try:
        job_posting = client.put(f"{RESOURCE_PATH}{job_posting_id}", json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nJob posting updated:")
    _print(job_posting)


def delete(client: ApiClient):
    print("\n-- Delete Job Posting --")
    job_posting_id = prompts.prompt_required_uuid("Job posting ID")
    if not prompts.confirm(f"Delete job posting {job_posting_id}?"):
        print("Cancelled.")
        return
    try:
        client.delete(f"{RESOURCE_PATH}{job_posting_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("Job posting deleted.")


_ACTIONS = [
    ("1", "Create job posting", create),
    ("2", "Get job posting by ID", get_by_id),
    ("3", "List all job postings", get_all),
    ("4", "Update job posting", update),
    ("5", "Delete job posting", delete),
]


def menu(client: ApiClient):
    while True:
        choice = prompts.prompt_menu(
            "Job Postings",
            [(k, l) for k, l, _ in _ACTIONS] + [("b", "Back")],
        )
        if choice == "b":
            return
        action = next((fn for k, _, fn in _ACTIONS if k == choice), None)
        if action is None:
            print("Invalid choice, try again.")
            continue
        action(client)
