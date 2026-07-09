from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Tuple


DEFAULT_POLICY = {
    "allowed_read_paths": ["allowed_docs/"],
    "blocked_read_paths": ["secrets/"],
    "allowed_write_paths": ["allowed_output/", "logs/"],
    "network_access": False,
}


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith(("'", '"')) and value.endswith(("'", '"')):
        return value[1:-1]
    return value


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    current_key: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith("  - "):
            if current_key is None:
                raise ValueError("Malformed YAML list entry")
            parsed.setdefault(current_key, []).append(_parse_scalar(stripped[4:]))
            continue
        if ":" not in line:
            raise ValueError(f"Unsupported YAML line: {line}")
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not value:
            parsed[key] = []
            current_key = key
        else:
            parsed[key] = _parse_scalar(value)
            current_key = None
    return parsed


def _load_policy(root_dir: Path) -> dict[str, Any]:
    policy_path = root_dir / "policy.yaml"
    if not policy_path.exists():
        return dict(DEFAULT_POLICY)

    try:
        raw = policy_path.read_text(encoding="utf-8")
        parsed = _parse_simple_yaml(raw)
    except Exception:
        return dict(DEFAULT_POLICY)

    policy = dict(DEFAULT_POLICY)
    for key in ("allowed_read_paths", "blocked_read_paths", "allowed_write_paths"):
        if key in parsed:
            value = parsed[key]
            if isinstance(value, str):
                policy[key] = [value]
            elif isinstance(value, list):
                policy[key] = value
    if "network_access" in parsed:
        policy["network_access"] = bool(parsed["network_access"])
    return policy


def _normalize_policy_paths(paths: Any) -> list[str]:
    if isinstance(paths, str):
        paths = [paths]
    normalized: list[str] = []
    for raw in paths or []:
        value = str(raw).strip().replace("\\", "/")
        if value.startswith("./"):
            value = value[2:]
        if value.endswith("/") and len(value) > 1:
            value = value.rstrip("/")
        normalized.append(value)
    return normalized


def _is_within(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def _is_allowed_write(path: Path, root_dir: Path, allowed_paths: list[str]) -> bool:
    try:
        relative_path = path.resolve().relative_to(root_dir.resolve()).as_posix()
    except ValueError:
        return False
    for allowed in allowed_paths:
        normalized = allowed.strip().replace("\\", "/").rstrip("/")
        if not normalized:
            continue
        if relative_path == normalized or relative_path.startswith(normalized + "/"):
            return True
    return False


def _is_blocked(path: Path, root_dir: Path, blocked_paths: list[str]) -> bool:
    try:
        relative_path = path.relative_to(root_dir).as_posix()
    except ValueError:
        return True
    for blocked in blocked_paths:
        normalized = blocked.strip().replace("\\", "/").rstrip("/")
        if not normalized:
            continue
        if relative_path == normalized or relative_path.startswith(normalized + "/"):
            return True
    return False


def _is_allowed_read(path: Path, root_dir: Path, allowed_paths: list[str]) -> bool:
    try:
        relative_path = path.relative_to(root_dir).as_posix()
    except ValueError:
        return False
    for allowed in allowed_paths:
        normalized = allowed.strip().replace("\\", "/").rstrip("/")
        if not normalized:
            continue
        if relative_path == normalized or relative_path.startswith(normalized + "/"):
            return True
    return False


def _is_secret_request(prompt: str) -> bool:
    lowered = prompt.lower()
    secret_terms = ["secret", "secrets", "token", "password", "api key", "credential"]
    return any(term in lowered for term in secret_terms)


def _is_network_request(prompt: str) -> bool:
    lowered = prompt.lower()
    terms = ["network", "internet", "download", "fetch", "http", "https", "url", "remote", "web"]
    return any(term in lowered for term in terms)


def _resolve_target_path(prompt: str, root_dir: Path) -> Path | None:
    tokens = re.findall(r"[A-Za-z0-9._/-]+", prompt)
    for token in tokens:
        normalized = token.replace("\\", "/")
        if normalized in {"read", "open", "show", "summarize", "the", "and", "for"}:
            continue
        candidates = [root_dir / normalized]
        if "/" not in normalized:
            candidates.append(root_dir / "allowed_docs" / normalized)
            candidates.append(root_dir / "secrets" / normalized)
        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                return candidate
    return None


def _read_allowed_docs(root_dir: Path, policy: dict[str, Any]) -> str:
    allowed_paths = _normalize_policy_paths(policy.get("allowed_read_paths"))
    blocked_paths = _normalize_policy_paths(policy.get("blocked_read_paths"))
    docs: list[str] = []
    for allowed in allowed_paths:
        base = root_dir / allowed
        if not base.exists():
            continue
        if base.is_file():
            if _is_blocked(base, root_dir, blocked_paths):
                continue
            docs.append(base.read_text(encoding="utf-8"))
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if _is_blocked(path, root_dir, blocked_paths):
                continue
            if not _is_allowed_read(path, root_dir, allowed_paths):
                continue
            docs.append(path.read_text(encoding="utf-8"))
    if not docs:
        return "No allowed documents were found."
    return "\n\n".join(docs)


def run_agent(
    prompt: str,
    root_dir: Path | str | None = None,
    report_path: Path | str | None = None,
    log_path: Path | str | None = None,
) -> Tuple[Path, Path]:
    root_path = Path(root_dir or Path(__file__).resolve().parent.parent)
    policy = _load_policy(root_path)
    policy["allowed_read_paths"] = _normalize_policy_paths(policy.get("allowed_read_paths"))
    policy["blocked_read_paths"] = _normalize_policy_paths(policy.get("blocked_read_paths"))
    policy["allowed_write_paths"] = _normalize_policy_paths(policy.get("allowed_write_paths"))

    output_dir = root_path / "allowed_output"
    logs_dir = root_path / "logs"
    _ensure_dir(output_dir)
    _ensure_dir(logs_dir)

    default_report_path = output_dir / "project_report.md"
    default_log_path = logs_dir / "audit.log"
    resolved_report_path = Path(report_path or default_report_path)
    resolved_log_path = Path(log_path or default_log_path)

    if _is_secret_request(prompt):
        report_text = (
            "# Project Report\n\n"
            "Refused: the request targeted restricted secrets content.\n"
        )
        action = "refused secrets-targeted request"
    elif policy.get("network_access") is False and _is_network_request(prompt):
        report_text = "# Project Report\n\nRefused: network access is disabled by policy.\n"
        action = "refused network request"
    else:
        target_path = _resolve_target_path(prompt, root_path)
        if target_path is not None:
            if _is_blocked(target_path, root_path, policy["blocked_read_paths"]):
                report_text = (
                    "# Project Report\n\n"
                    "Refused: the request targeted restricted secrets content.\n"
                )
                action = "refused secrets-targeted request"
            else:
                contents = target_path.read_text(encoding="utf-8")
                report_text = (
                    "# Project Report\n\n"
                    f"Prompt: {prompt}\n\n"
                    f"Requested file contents:\n{contents}\n"
                )
                action = "read requested file"
        else:
            contents = _read_allowed_docs(root_path, policy)
            report_text = (
                "# Project Report\n\n"
                f"Prompt: {prompt}\n\n"
                f"Allowed documents summary:\n{contents}\n"
            )
            action = "processed allowed documents"

    report_write_allowed = _is_allowed_write(resolved_report_path, root_path, policy["allowed_write_paths"])
    log_write_allowed = _is_allowed_write(resolved_log_path, root_path, policy["allowed_write_paths"])

    if not report_write_allowed:
        report_text += "\nWrite blocked: report path is outside the allowed write paths.\n"
        resolved_report_path = default_report_path

    if not log_write_allowed:
        report_text += "\nWrite blocked: log path is outside the allowed write paths.\n"
        resolved_log_path = default_log_path

    resolved_report_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_report_path.write_text(report_text, encoding="utf-8")

    resolved_log_path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(report_text.encode("utf-8")).hexdigest()[:12]
    log_entry = f"[{action}] prompt={prompt!r} report={resolved_report_path.name} digest={digest}\n"
    with resolved_log_path.open("a", encoding="utf-8") as handle:
        handle.write(log_entry)

    return resolved_report_path, resolved_log_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the safe agent")
    parser.add_argument("prompt", nargs="?", default="Summarize the approved documents")
    parser.add_argument("--root", default=None)
    args = parser.parse_args()

    run_agent(args.prompt, args.root)
