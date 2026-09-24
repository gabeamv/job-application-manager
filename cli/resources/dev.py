from getpass import getpass

from cli import prompts
from cli.http_client import ApiClient, ApiError

RESOURCE_PATH = "/api/dev"


def _auth_headers() -> dict:
    secret = getpass("Dev secret (X-Dev-Secret, input hidden): ")
    return {"X-Dev-Secret": secret}


def health_check(client: ApiClient):
    print("\n-- Health Check --")
    try:
        result = client.get(f"{RESOURCE_PATH}/healthz", headers=_auth_headers())
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print(result)


def reset_db(client: ApiClient):
    print("\n-- Reset Database --")
    print("This permanently deletes ALL data in every table.")
    if not prompts.confirm("Are you sure you want to reset the database?"):
        print("Cancelled.")
        return
    try:
        result = client.delete(f"{RESOURCE_PATH}/reset", headers=_auth_headers())
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print(result)


_ACTIONS = [
    ("1", "Health check", health_check),
    ("2", "Reset database (destructive)", reset_db),
]


def menu(client: ApiClient):
    while True:
        choice = prompts.prompt_menu(
            "Dev Tools",
            [(k, l) for k, l, _ in _ACTIONS] + [("b", "Back")],
        )
        if choice == "b":
            return
        action = next((fn for k, _, fn in _ACTIONS if k == choice), None)
        if action is None:
            print("Invalid choice, try again.")
            continue
        action(client)
