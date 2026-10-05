from datetime import date, datetime
from uuid import UUID

# Sentinel returned by prompt_update_* helpers when the user left a field
# blank, meaning "leave this field unchanged" rather than "set it to null".
UNSET = object()

# Typing this at any field prompt aborts the current action.
BACK = "/back"


class Cancelled(Exception):
    pass


def _ask(prompt: str) -> str:
    value = input(prompt).strip()
    if value.lower() == BACK:
        raise Cancelled
    return value


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
        value = _ask(f"{label}: ")
        if value:
            return value
        print("This field is required.")


def prompt_optional_str(label: str) -> str | None:
    value = _ask(f"{label} (optional, Enter for none): ")
    return value or None


def prompt_required_float(label: str) -> float:
    while True:
        raw = _ask(f"{label}: ")
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def prompt_optional_float(label: str) -> float | None:
    while True:
        raw = _ask(f"{label} (optional, Enter for none): ")
        if not raw:
            return None
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def prompt_required_uuid(label: str) -> UUID:
    while True:
        raw = _ask(f"{label}: ")
        try:
            return UUID(raw)
        except ValueError:
            print("Please enter a valid UUID.")


def prompt_optional_uuid(label: str) -> UUID | None:
    while True:
        raw = _ask(f"{label} (optional, Enter for none): ")
        if not raw:
            return None
        try:
            return UUID(raw)
        except ValueError:
            print("Please enter a valid UUID.")


def prompt_required_date(label: str) -> date:
    while True:
        raw = _ask(f"{label} (YYYY-MM-DD): ")
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("Please enter a valid date as YYYY-MM-DD.")


def prompt_optional_date(label: str) -> date | None:
    while True:
        raw = _ask(f"{label} (YYYY-MM-DD, optional, Enter for none): ")
        if not raw:
            return None
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("Please enter a valid date as YYYY-MM-DD.")


def prompt_optional_datetime(label: str) -> datetime | None:
    while True:
        raw = _ask(f"{label} (YYYY-MM-DD HH:MM, optional, Enter for none): ")
        if not raw:
            return None
        try:
            return datetime.fromisoformat(raw)
        except ValueError:
            print("Please enter a valid datetime as YYYY-MM-DD HH:MM.")


def prompt_update_str(label: str):
    raw = _ask(f"{label} (Enter to leave unchanged): ")
    return raw if raw else UNSET


def prompt_update_float(label: str):
    while True:
        raw = _ask(f"{label} (Enter to leave unchanged): ")
        if not raw:
            return UNSET
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def prompt_update_uuid(label: str):
    while True:
        raw = _ask(f"{label} (Enter to leave unchanged): ")
        if not raw:
            return UNSET
        try:
            return UUID(raw)
        except ValueError:
            print("Please enter a valid UUID.")


def prompt_update_date(label: str):
    while True:
        raw = _ask(f"{label} (YYYY-MM-DD, Enter to leave unchanged): ")
        if not raw:
            return UNSET
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("Please enter a valid date as YYYY-MM-DD.")


def prompt_update_datetime(label: str):
    while True:
        raw = _ask(f"{label} (YYYY-MM-DD HH:MM, Enter to leave unchanged): ")
        if not raw:
            return UNSET
        try:
            return datetime.fromisoformat(raw)
        except ValueError:
            print("Please enter a valid datetime as YYYY-MM-DD HH:MM.")
