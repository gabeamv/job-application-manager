from cli import prompts
from cli.http_client import ApiClient, ApiError
from cli.prompts import UNSET
from cli.serialize import to_payload

RESOURCE_PATH = "/api/applications/"


def _print(application: dict):
    print(f"  id:              {application['id']}")
    print(f"  job_postings_id: {application['job_postings_id']}")
    print(f"  resumes_id:      {application['resumes_id']}")
    print(f"  date_applied:    {application['date_applied']}")
    print(f"  status:          {application.get('status') or '-'}")
    print(f"  created_at:      {application.get('created_at') or '-'}")
    print(f"  updated_at:      {application.get('updated_at') or '-'}")


def create(client: ApiClient):
    print("\n-- Create Application --")
    payload = to_payload({
        "job_postings_id": prompts.prompt_required_uuid("Job posting ID"),
        "resumes_id": prompts.prompt_required_uuid("Resume ID"),
        "date_applied": prompts.prompt_required_date("Date applied"),
        "status": prompts.prompt_optional_str("Status"),
    })
    try:
        application = client.post(RESOURCE_PATH, json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nApplication created:")
    _print(application)


def get_by_id(client: ApiClient):
    print("\n-- Get Application by ID --")
    application_id = prompts.prompt_required_uuid("Application ID")
    try:
        application = client.get(f"{RESOURCE_PATH}{application_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print()
    _print(application)


def get_all(client: ApiClient):
    print("\n-- All Applications --")
    try:
        applications = client.get(RESOURCE_PATH)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    if not applications:
        print("No applications found.")
        return
    for application in applications:
        _print(application)
        print()


def update(client: ApiClient):
    print("\n-- Update Application --")
    application_id = prompts.prompt_required_uuid("Application ID")

    fields = {
        "job_postings_id": prompts.prompt_update_uuid("Job posting ID"),
        "resumes_id": prompts.prompt_update_uuid("Resume ID"),
        "date_applied": prompts.prompt_update_date("Date applied"),
        "status": prompts.prompt_update_str("Status"),
    }
    payload = to_payload({k: v for k, v in fields.items() if v is not UNSET})

    if not payload:
        print("No changes entered.")
        return
    try:
        application = client.put(f"{RESOURCE_PATH}{application_id}", json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nApplication updated:")
    _print(application)


def delete(client: ApiClient):
    print("\n-- Delete Application --")
    application_id = prompts.prompt_required_uuid("Application ID")
    if not prompts.confirm(f"Delete application {application_id}?"):
        print("Cancelled.")
        return
    try:
        client.delete(f"{RESOURCE_PATH}{application_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("Application deleted.")


_ACTIONS = [
    ("1", "Create application", create),
    ("2", "Get application by ID", get_by_id),
    ("3", "List all applications", get_all),
    ("4", "Update application", update),
    ("5", "Delete application", delete),
]


def menu(client: ApiClient):
    while True:
        choice = prompts.prompt_menu(
            "Applications",
            [(k, l) for k, l, _ in _ACTIONS] + [("b", "Back")],
        )
        if choice == "b":
            return
        action = next((fn for k, _, fn in _ACTIONS if k == choice), None)
        if action is None:
            print("Invalid choice, try again.")
            continue
        action(client)
