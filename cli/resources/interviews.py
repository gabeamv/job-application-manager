from cli import prompts
from cli.http_client import ApiClient, ApiError
from cli.prompts import UNSET
from cli.serialize import to_payload

RESOURCE_PATH = "/api/interviews/"


def _print(interview: dict):
    print(f"  id:             {interview['id']}")
    print(f"  applications_id:{interview['applications_id']}")
    print(f"  type:           {interview.get('type') or '-'}")
    print(f"  scheduled_at:   {interview.get('scheduled_at') or '-'}")
    print(f"  notes:          {interview.get('notes') or '-'}")
    print(f"  created_at:     {interview.get('created_at') or '-'}")


def create(client: ApiClient):
    print("\n-- Create Interview --")
    payload = to_payload({
        "applications_id": prompts.prompt_required_uuid("Application ID"),
        "type": prompts.prompt_optional_str("Type"),
        "scheduled_at": prompts.prompt_optional_datetime("Scheduled at"),
        "notes": prompts.prompt_optional_str("Notes"),
    })
    try:
        interview = client.post(RESOURCE_PATH, json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nInterview created:")
    _print(interview)


def get_by_id(client: ApiClient):
    print("\n-- Get Interview by ID --")
    interview_id = prompts.prompt_required_uuid("Interview ID")
    try:
        interview = client.get(f"{RESOURCE_PATH}{interview_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print()
    _print(interview)


def get_all(client: ApiClient):
    print("\n-- All Interviews --")
    try:
        interviews = client.get(RESOURCE_PATH)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    if not interviews:
        print("No interviews found.")
        return
    for interview in interviews:
        _print(interview)
        print()


def update(client: ApiClient):
    print("\n-- Update Interview --")
    interview_id = prompts.prompt_required_uuid("Interview ID")

    fields = {
        "applications_id": prompts.prompt_update_uuid("Application ID"),
        "type": prompts.prompt_update_str("Type"),
        "scheduled_at": prompts.prompt_update_datetime("Scheduled at"),
        "notes": prompts.prompt_update_str("Notes"),
    }
    payload = to_payload({k: v for k, v in fields.items() if v is not UNSET})

    if not payload:
        print("No changes entered.")
        return
    try:
        interview = client.put(f"{RESOURCE_PATH}{interview_id}", json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nInterview updated:")
    _print(interview)


def delete(client: ApiClient):
    print("\n-- Delete Interview --")
    interview_id = prompts.prompt_required_uuid("Interview ID")
    if not prompts.confirm(f"Delete interview {interview_id}?"):
        print("Cancelled.")
        return
    try:
        client.delete(f"{RESOURCE_PATH}{interview_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("Interview deleted.")


_ACTIONS = [
    ("1", "Create interview", create),
    ("2", "Get interview by ID", get_by_id),
    ("3", "List all interviews", get_all),
    ("4", "Update interview", update),
    ("5", "Delete interview", delete),
]


def menu(client: ApiClient):
    while True:
        choice = prompts.prompt_menu(
            "Interviews",
            [(k, l) for k, l, _ in _ACTIONS] + [("b", "Back")],
        )
        if choice == "b":
            return
        action = next((fn for k, _, fn in _ACTIONS if k == choice), None)
        if action is None:
            print("Invalid choice, try again.")
            continue
        action(client)
