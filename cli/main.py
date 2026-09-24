from cli import prompts
from cli.http_client import ApiClient
from cli.resources import (
    applications,
    companies,
    cover_letters,
    dev,
    interviews,
    job_postings,
    job_postings_skills,
    resumes,
    skills,
)

DEFAULT_BASE_URL = "http://127.0.0.1:8000"

_RESOURCES = [
    ("1", "Companies", companies.menu),
    ("2", "Job postings", job_postings.menu),
    ("3", "Job posting skills", job_postings_skills.menu),
    ("4", "Resumes", resumes.menu),
    ("5", "Cover letters", cover_letters.menu),
    ("6", "Skills", skills.menu),
    ("7", "Interviews", interviews.menu),
    ("8", "Applications", applications.menu),
    ("9", "Dev tools", dev.menu),
]


def main():
    print("Job Application Manager - API Test Client")
    base_url = input(f"API base URL [{DEFAULT_BASE_URL}]: ").strip() or DEFAULT_BASE_URL

    client = ApiClient(base_url)
    try:
        while True:
            choice = prompts.prompt_menu(
                "Select a resource",
                [(k, l) for k, l, _ in _RESOURCES] + [("q", "Quit")],
            )
            if choice == "q":
                print("Goodbye.")
                return
            action = next((fn for k, _, fn in _RESOURCES if k == choice), None)
            if action is None:
                print("Invalid choice, try again.")
                continue
            action(client)
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
    finally:
        client.close()


if __name__ == "__main__":
    main()
