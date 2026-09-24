from cli import prompts
from cli.http_client import ApiClient, ApiError
from cli.prompts import UNSET
from cli.serialize import to_payload

RESOURCE_PATH = "/api/resumes/"


def _print(resume: dict):
    print(f"  id:      {resume['id']}")
    print(f"  name:    {resume['name']}")
    print(f"  version: {resume['version']}")
    print(f"  url:     {resume['url']}")


def create(client: ApiClient):
    print("\n-- Create Resume --")
    payload = to_payload({
        "name": prompts.prompt_required_str("Name"),
        "version": prompts.prompt_required_float("Version"),
        "url": prompts.prompt_required_str("URL"),
    })
    try:
        resume = client.post(RESOURCE_PATH, json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nResume created:")
    _print(resume)


def get_by_id(client: ApiClient):
    print("\n-- Get Resume by ID --")
    resume_id = prompts.prompt_required_uuid("Resume ID")
    try:
        resume = client.get(f"{RESOURCE_PATH}{resume_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print()
    _print(resume)


def get_all(client: ApiClient):
    print("\n-- All Resumes --")
    try:
        resumes = client.get(RESOURCE_PATH)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    if not resumes:
        print("No resumes found.")
        return
    for resume in resumes:
        _print(resume)
        print()


def update(client: ApiClient):
    print("\n-- Update Resume --")
    resume_id = prompts.prompt_required_uuid("Resume ID")

    fields = {
        "name": prompts.prompt_update_str("Name"),
        "version": prompts.prompt_update_float("Version"),
        "url": prompts.prompt_update_str("URL"),
    }
    payload = to_payload({k: v for k, v in fields.items() if v is not UNSET})

    if not payload:
        print("No changes entered.")
        return
    try:
        resume = client.put(f"{RESOURCE_PATH}{resume_id}", json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nResume updated:")
    _print(resume)


def delete(client: ApiClient):
    print("\n-- Delete Resume --")
    resume_id = prompts.prompt_required_uuid("Resume ID")
    if not prompts.confirm(f"Delete resume {resume_id}?"):
        print("Cancelled.")
        return
    try:
        client.delete(f"{RESOURCE_PATH}{resume_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("Resume deleted.")


_ACTIONS = [
    ("1", "Create resume", create),
    ("2", "Get resume by ID", get_by_id),
    ("3", "List all resumes", get_all),
    ("4", "Update resume", update),
    ("5", "Delete resume", delete),
]


def menu(client: ApiClient):
    while True:
        choice = prompts.prompt_menu(
            "Resumes",
            [(k, l) for k, l, _ in _ACTIONS] + [("b", "Back")],
        )
        if choice == "b":
            return
        action = next((fn for k, _, fn in _ACTIONS if k == choice), None)
        if action is None:
            print("Invalid choice, try again.")
            continue
        action(client)
