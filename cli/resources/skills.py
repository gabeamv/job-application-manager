from cli import prompts
from cli.http_client import ApiClient, ApiError
from cli.prompts import UNSET
from cli.serialize import to_payload

RESOURCE_PATH = "/api/skills/"


def _print(skill: dict):
    print(f"  id:          {skill['id']}")
    print(f"  name:        {skill['name']}")
    print(f"  description: {skill.get('description') or '-'}")


def create(client: ApiClient):
    print("\n-- Create Skill --")
    payload = to_payload({
        "name": prompts.prompt_required_str("Name"),
        "description": prompts.prompt_optional_str("Description"),
    })
    try:
        skill = client.post(RESOURCE_PATH, json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nSkill created:")
    _print(skill)


def get_by_id(client: ApiClient):
    print("\n-- Get Skill by ID --")
    skill_id = prompts.prompt_required_uuid("Skill ID")
    try:
        skill = client.get(f"{RESOURCE_PATH}{skill_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print()
    _print(skill)


def get_all(client: ApiClient):
    print("\n-- All Skills --")
    try:
        skills = client.get(RESOURCE_PATH)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    if not skills:
        print("No skills found.")
        return
    for skill in skills:
        _print(skill)
        print()


def update(client: ApiClient):
    print("\n-- Update Skill --")
    skill_id = prompts.prompt_required_uuid("Skill ID")

    fields = {
        "name": prompts.prompt_update_str("Name"),
        "description": prompts.prompt_update_str("Description"),
    }
    payload = to_payload({k: v for k, v in fields.items() if v is not UNSET})

    if not payload:
        print("No changes entered.")
        return
    try:
        skill = client.put(f"{RESOURCE_PATH}{skill_id}", json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nSkill updated:")
    _print(skill)


def delete(client: ApiClient):
    print("\n-- Delete Skill --")
    skill_id = prompts.prompt_required_uuid("Skill ID")
    if not prompts.confirm(f"Delete skill {skill_id}?"):
        print("Cancelled.")
        return
    try:
        client.delete(f"{RESOURCE_PATH}{skill_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("Skill deleted.")


_ACTIONS = [
    ("1", "Create skill", create),
    ("2", "Get skill by ID", get_by_id),
    ("3", "List all skills", get_all),
    ("4", "Update skill", update),
    ("5", "Delete skill", delete),
]


def menu(client: ApiClient):
    while True:
        choice = prompts.prompt_menu(
            "Skills",
            [(k, l) for k, l, _ in _ACTIONS] + [("b", "Back")],
        )
        if choice == "b":
            return
        action = next((fn for k, _, fn in _ACTIONS if k == choice), None)
        if action is None:
            print("Invalid choice, try again.")
            continue
        action(client)
