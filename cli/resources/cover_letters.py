from cli import prompts
from cli.http_client import ApiClient, ApiError
from cli.prompts import UNSET
from cli.serialize import to_payload

RESOURCE_PATH = "/api/cover_letters/"


def _print(cover_letter: dict):
    print(f"  id:              {cover_letter['id']}")
    print(f"  job_postings_id: {cover_letter['job_postings_id']}")
    print(f"  name:            {cover_letter['name']}")
    print(f"  url:             {cover_letter['url']}")


def create(client: ApiClient):
    print("\n-- Create Cover Letter --")
    payload = to_payload({
        "job_postings_id": prompts.prompt_required_uuid("Job posting ID"),
        "name": prompts.prompt_required_str("Name"),
        "url": prompts.prompt_required_str("URL"),
    })
    try:
        cover_letter = client.post(RESOURCE_PATH, json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nCover letter created:")
    _print(cover_letter)


def get_by_id(client: ApiClient):
    print("\n-- Get Cover Letter by ID --")
    cover_letter_id = prompts.prompt_required_uuid("Cover letter ID")
    try:
        cover_letter = client.get(f"{RESOURCE_PATH}{cover_letter_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print()
    _print(cover_letter)


def get_all(client: ApiClient):
    print("\n-- All Cover Letters --")
    try:
        cover_letters = client.get(RESOURCE_PATH)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    if not cover_letters:
        print("No cover letters found.")
        return
    for cover_letter in cover_letters:
        _print(cover_letter)
        print()


def update(client: ApiClient):
    print("\n-- Update Cover Letter --")
    cover_letter_id = prompts.prompt_required_uuid("Cover letter ID")

    fields = {
        "job_postings_id": prompts.prompt_update_uuid("Job posting ID"),
        "name": prompts.prompt_update_str("Name"),
        "url": prompts.prompt_update_str("URL"),
    }
    payload = to_payload({k: v for k, v in fields.items() if v is not UNSET})

    if not payload:
        print("No changes entered.")
        return
    try:
        cover_letter = client.put(f"{RESOURCE_PATH}{cover_letter_id}", json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nCover letter updated:")
    _print(cover_letter)


def delete(client: ApiClient):
    print("\n-- Delete Cover Letter --")
    cover_letter_id = prompts.prompt_required_uuid("Cover letter ID")
    if not prompts.confirm(f"Delete cover letter {cover_letter_id}?"):
        print("Cancelled.")
        return
    try:
        client.delete(f"{RESOURCE_PATH}{cover_letter_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("Cover letter deleted.")


_ACTIONS = [
    ("1", "Create cover letter", create),
    ("2", "Get cover letter by ID", get_by_id),
    ("3", "List all cover letters", get_all),
    ("4", "Update cover letter", update),
    ("5", "Delete cover letter", delete),
]


def menu(client: ApiClient):
    while True:
        choice = prompts.prompt_menu(
            "Cover Letters",
            [(k, l) for k, l, _ in _ACTIONS] + [("b", "Back")],
        )
        if choice == "b":
            return
        action = next((fn for k, _, fn in _ACTIONS if k == choice), None)
        if action is None:
            print("Invalid choice, try again.")
            continue
        action(client)
