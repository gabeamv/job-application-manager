from cli import prompts
from cli.http_client import ApiClient, ApiError
from cli.prompts import UNSET
from cli.serialize import to_payload

RESOURCE_PATH = "/api/companies/"


def _print(company: dict):
    print(f"  id:       {company['id']}")
    print(f"  name:     {company['name']}")
    print(f"  url:      {company.get('url') or '-'}")
    print(f"  industry: {company.get('industry') or '-'}")


def create(client: ApiClient):
    print("\n-- Create Company -- (type /back to cancel)")
    payload = to_payload({
        "name": prompts.prompt_required_str("Name"),
        "url": prompts.prompt_optional_str("URL"),
        "industry": prompts.prompt_optional_str("Industry"),
    })
    try:
        company = client.post(RESOURCE_PATH, json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nCompany created:")
    _print(company)


def get_by_id(client: ApiClient):
    print("\n-- Get Company by ID -- (type /back to cancel)")
    company_id = prompts.prompt_required_uuid("Company ID")
    try:
        company = client.get(f"{RESOURCE_PATH}{company_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print()
    _print(company)


def get_by_name(client: ApiClient):
    print("\n-- Get Company by Name -- (type /back to cancel)")
    name = prompts.prompt_required_str("Company name")
    try:
        company = client.get(f"{RESOURCE_PATH}by-name", params={"name": name})
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print()
    _print(company)


def get_all(client: ApiClient):
    print("\n-- All Companies --")
    try:
        companies = client.get(RESOURCE_PATH)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    if not companies:
        print("No companies found.")
        return
    for company in companies:
        _print(company)
        print()


def update(client: ApiClient):
    print("\n-- Update Company -- (type /back to cancel)")
    company_id = prompts.prompt_required_uuid("Company ID")

    fields = {
        "name": prompts.prompt_update_str("Name"),
        "url": prompts.prompt_update_str("URL"),
        "industry": prompts.prompt_update_str("Industry"),
    }
    payload = to_payload({k: v for k, v in fields.items() if v is not UNSET})

    if not payload:
        print("No changes entered.")
        return
    try:
        company = client.put(f"{RESOURCE_PATH}{company_id}", json=payload)
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nCompany updated:")
    _print(company)


def update_by_name(client: ApiClient):
    print("\n-- Update Company by Name -- (type /back to cancel)")
    lookup_name = prompts.prompt_required_str("Current company name")

    fields = {
        "name": prompts.prompt_update_str("Name"),
        "url": prompts.prompt_update_str("URL"),
        "industry": prompts.prompt_update_str("Industry"),
    }
    payload = to_payload({k: v for k, v in fields.items() if v is not UNSET})

    if not payload:
        print("No changes entered.")
        return
    try:
        company = client.put(f"{RESOURCE_PATH}by-name", json=payload, params={"name": lookup_name})
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("\nCompany updated:")
    _print(company)


def delete(client: ApiClient):
    print("\n-- Delete Company -- (type /back to cancel)")
    company_id = prompts.prompt_required_uuid("Company ID")
    if not prompts.confirm(f"Delete company {company_id}?"):
        print("Cancelled.")
        return
    try:
        client.delete(f"{RESOURCE_PATH}{company_id}")
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("Company deleted.")


def delete_by_name(client: ApiClient):
    print("\n-- Delete Company by Name -- (type /back to cancel)")
    name = prompts.prompt_required_str("Company name")
    if not prompts.confirm(f"Delete company {name}?"):
        print("Cancelled.")
        return
    try:
        client.delete(f"{RESOURCE_PATH}by-name", params={"name": name})
    except ApiError as exc:
        print(f"Error: {exc}")
        return
    print("Company deleted.")


_ACTIONS = [
    ("1", "Create company", create),
    ("2", "Get company by ID", get_by_id),
    ("3", "Get company by name", get_by_name),
    ("4", "List all companies", get_all),
    ("5", "Update company", update),
    ("6", "Update company by name", update_by_name),
    ("7", "Delete company", delete),
    ("8", "Delete company by name", delete_by_name),
]


def menu(client: ApiClient):
    while True:
        choice = prompts.prompt_menu(
            "Companies",
            [(k, l) for k, l, _ in _ACTIONS] + [("b", "Back")],
        )
        if choice == "b":
            return
        action = next((fn for k, _, fn in _ACTIONS if k == choice), None)
        if action is None:
            print("Invalid choice, try again.")
            continue
        try:
            action(client)
        except prompts.Cancelled:
            print("Cancelled.")
