from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
ALLOWED_DOCS = BASE_DIR / "allowed_docs"
SECRETS = BASE_DIR / "secrets"
OUTPUT = BASE_DIR / "allowed_output"
LOGS = BASE_DIR / "logs"

OUTPUT.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)

def audit(message: str):
    with open(LOGS / "audit.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {message}\n")

def safe_read(path: Path) -> str:
    resolved = path.resolve()

    if str(resolved).startswith(str(SECRETS.resolve())):
        audit(f"BLOCKED read attempt: {resolved}")
        raise PermissionError("Blocked: agent is not allowed to read secrets/")

    if not str(resolved).startswith(str(ALLOWED_DOCS.resolve())):
        audit(f"BLOCKED read attempt outside allowed_docs: {resolved}")
        raise PermissionError("Blocked: agent can only read allowed_docs/")

    audit(f"READ allowed file: {resolved}")
    return path.read_text(encoding="utf-8")

def main():
    notes_file = ALLOWED_DOCS / "sample_project_notes.txt"
    content = safe_read(notes_file)

    report = f"""# Project Report

## Summary
The agent read the allowed project notes and generated this report.

## Source content
{content}

## Safety status
- Read allowed_docs/: yes
- Read secrets/: no
- Network access: disabled by policy
- Audit log: enabled
"""

    output_file = OUTPUT / "project_report.md"
    output_file.write_text(report, encoding="utf-8")
    audit(f"WROTE report: {output_file.resolve()}")

    print("✅ Report created:", output_file)
    print("✅ Audit log updated:", LOGS / "audit.log")

if __name__ == "__main__":
    main()
