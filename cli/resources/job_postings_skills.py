from cli import prompts
from cli.http_client import ApiClient, ApiError
from cli.prompts import UNSET
from cli.serialize import to_payload

RESOURCE_PATH = "/api/job_postings_skills/"


def _print(link: dict):
    print(f"  id:               {link['id']}")
    print(f"  job_postings_id:  {link['job_postings_id']}")
    print(f"  skills_id:        {link['skills_id']}")


def create(client: ApiClient):
    print("\n-- Link Skill to Job Posting --")
    payload = to_payload({
        "job_postings_id": prompts.prompt_required_uuid("Job posting ID"),
        "skills_id": prompts.prompt_required_uuid("Skill ID"),
    })
    try:
        link = client.post(RESOURCE_PATH, json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nJob posting skill created:")
    _print(link)


def get_by_id(client: ApiClient):
    print("\n-- Get Job Posting Skill by ID --")
    link_id = prompts.prompt_required_uuid("Job posting skill ID")
    try:
        link = client.get(f"{RESOURCE_PATH}{link_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print()
    _print(link)


def get_all(client: ApiClient):
    print("\n-- All Job Posting Skills --")
    try:
        links = client.get(RESOURCE_PATH)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    if not links:
        print("No job posting skills found.")
        return
    for link in links:
        _print(link)
        print()


def update(client: ApiClient):
    print("\n-- Update Job Posting Skill --")
    link_id = prompts.prompt_required_uuid("Job posting skill ID")

    fields = {
        "job_postings_id": prompts.prompt_update_uuid("Job posting ID"),
        "skills_id": prompts.prompt_update_uuid("Skill ID"),
    }
    payload = to_payload({k: v for k, v in fields.items() if v is not UNSET})

    if not payload:
        print("No changes entered.")
        return
    try:
        link = client.put(f"{RESOURCE_PATH}{link_id}", json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nJob posting skill updated:")
    _print(link)


def delete(client: ApiClient):
    print("\n-- Delete Job Posting Skill --")
    link_id = prompts.prompt_required_uuid("Job posting skill ID")
    if not prompts.confirm(f"Delete job posting skill {link_id}?"):
        print("Cancelled.")
        return
    try:
        client.delete(f"{RESOURCE_PATH}{link_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("Job posting skill deleted.")


_ACTIONS = [
    ("1", "Link skill to job posting", create),
    ("2", "Get job posting skill by ID", get_by_id),
    ("3", "List all job posting skills", get_all),
    ("4", "Update job posting skill", update),
    ("5", "Delete job posting skill", delete),
]


def menu(client: ApiClient):
    while True:
        choice = prompts.prompt_menu(
            "Job Posting Skills",
            [(k, l) for k, l, _ in _ACTIONS] + [("b", "Back")],
        )
        if choice == "b":
            return
        action = next((fn for k, _, fn in _ACTIONS if k == choice), None)
        if action is None:
            print("Invalid choice, try again.")
            continue
        action(client)
