from enum import StrEnum

class ApplicationStatus(StrEnum):
    PENDING_RESPONSE = "pending_response"
    REJECTED_GHOSTED = "rejected_ghosted"
    IN_HIRING_PROCESS = "in_hiring_process"
    REJECTED_AT_SCREENING = "rejected_at_screening"
    REJECTED_AT_INTERVIEW = "rejected_at_interview"
    RETURN_OFFER = "return_offer"

_status_values = ", ".join(f"'{s.value}'" for s in ApplicationStatus)