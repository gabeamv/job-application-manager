from datetime import date, datetime
from uuid import UUID

# Sentinel returned by prompt_update_* helpers when the user left a field
# blank, meaning "leave this field unchanged" rather than "set it to null".
UNSET = object()


def prompt_menu(title: str, options: list[tuple[str, str]]) -> str:
    print(f"\n{title}")
    for key, label in options:
        print(f"  [{key}] {label}")
    return input("> ").strip().lower()


def confirm(message: str) -> bool:
    answer = input(f"{message} [y/N]: ").strip().lower()
    return answer in ("y", "yes")


def prompt_required_str(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("This field is required.")


def prompt_optional_str(label: str) -> str | None:
    value = input(f"{label} (optional, Enter for none): ").strip()
    return value or None


def prompt_required_float(label: str) -> float:
    while True:
        raw = input(f"{label}: ").strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def prompt_optional_float(label: str) -> float | None:
    while True:
        raw = input(f"{label} (optional, Enter for none): ").strip()
        if not raw:
            return None
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def prompt_required_uuid(label: str) -> UUID:
    while True:
        raw = input(f"{label}: ").strip()
        try:
            return UUID(raw)
        except ValueError:
            print("Please enter a valid UUID.")


def prompt_optional_uuid(label: str) -> UUID | None:
    while True:
        raw = input(f"{label} (optional, Enter for none): ").strip()
        if not raw:
            return None
        try:
            return UUID(raw)
        except ValueError:
            print("Please enter a valid UUID.")


def prompt_required_date(label: str) -> date:
    while True:
        raw = input(f"{label} (YYYY-MM-DD): ").strip()
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("Please enter a valid date as YYYY-MM-DD.")


def prompt_optional_date(label: str) -> date | None:
    while True:
        raw = input(f"{label} (YYYY-MM-DD, optional, Enter for none): ").strip()
        if not raw:
            return None
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("Please enter a valid date as YYYY-MM-DD.")


def prompt_optional_datetime(label: str) -> datetime | None:
    while True:
        raw = input(f"{label} (YYYY-MM-DD HH:MM, optional, Enter for none): ").strip()
        if not raw:
            return None
        try:
            return datetime.fromisoformat(raw)
        except ValueError:
            print("Please enter a valid datetime as YYYY-MM-DD HH:MM.")


def prompt_update_str(label: str):
    raw = input(f"{label} (Enter to leave unchanged): ").strip()
    return raw if raw else UNSET


def prompt_update_float(label: str):
    while True:
        raw = input(f"{label} (Enter to leave unchanged): ").strip()
        if not raw:
            return UNSET
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def prompt_update_uuid(label: str):
    while True:
        raw = input(f"{label} (Enter to leave unchanged): ").strip()
        if not raw:
            return UNSET
        try:
            return UUID(raw)
        except ValueError:
            print("Please enter a valid UUID.")


def prompt_update_date(label: str):
    while True:
        raw = input(f"{label} (YYYY-MM-DD, Enter to leave unchanged): ").strip()
        if not raw:
            return UNSET
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("Please enter a valid date as YYYY-MM-DD.")


def prompt_update_datetime(label: str):
    while True:
        raw = input(f"{label} (YYYY-MM-DD HH:MM, Enter to leave unchanged): ").strip()
        if not raw:
            return UNSET
        try:
            return datetime.fromisoformat(raw)
        except ValueError:
            print("Please enter a valid datetime as YYYY-MM-DD HH:MM.")
