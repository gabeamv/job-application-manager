from datetime import date, datetime
from uuid import UUID


def jsonable(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def to_payload(fields: dict) -> dict:
    """Convert a dict of Python values into a JSON-serializable payload."""
    return {key: jsonable(value) for key, value in fields.items()}
