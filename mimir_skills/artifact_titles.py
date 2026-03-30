from __future__ import annotations

import re
from datetime import datetime
from typing import Any


_ACRONYM_TOKENS = {
    "ai": "AI",
    "api": "API",
    "aws": "AWS",
    "ci": "CI",
    "id": "ID",
    "pr": "PR",
    "sdk": "SDK",
    "tls": "TLS",
    "ui": "UI",
    "ux": "UX",
}


def decision_note_title(record: dict[str, Any]) -> str:
    return compose_display_title(
        date=best_date(record.get("timestamp"), fallback_id=record.get("id")),
        kind="Decision",
        subject=decision_subject(record),
    )


def decision_summary_title(record: dict[str, Any]) -> str:
    return compose_display_title(
        date=best_date(record.get("timestamp"), fallback_id=record.get("id")),
        kind="Decision Summary",
        subject=decision_subject(record),
    )


def memory_note_title(artifact: dict[str, Any]) -> str:
    status = artifact.get("status")
    status_label = "Memory"
    if isinstance(status, str) and status.strip():
        status_label = f"{humanize_token(status.strip())} Memory"

    return compose_display_title(
        date=best_date(
            artifact.get("validated_at"),
            artifact.get("last_validated_at"),
            artifact.get("created_at"),
            fallback_id=artifact.get("id"),
        ),
        kind=status_label,
        subject=memory_subject(artifact),
    )


def decision_subject(record: dict[str, Any]) -> str:
    task_ref = record.get("task_ref")
    if isinstance(task_ref, dict):
        raw_title = task_ref.get("title")
        if isinstance(raw_title, str) and raw_title.strip():
            return raw_title.strip()

    record_id = record.get("id")
    if isinstance(record_id, str) and record_id.strip():
        return subject_from_identifier(record_id)
    return ""


def memory_subject(artifact: dict[str, Any]) -> str:
    artifact_id = artifact.get("id")
    if isinstance(artifact_id, str) and artifact_id.strip():
        return subject_from_identifier(artifact_id)
    return ""


def compose_display_title(date: str, kind: str, subject: str) -> str:
    date_prefix = f"[{date}] " if date else ""
    if subject:
        return f"{date_prefix}{kind} - {subject}"
    return f"{date_prefix}{kind}"


def best_date(*values: Any, fallback_id: Any = None) -> str:
    for value in values:
        extracted = extract_display_date(value)
        if extracted:
            return extracted

    if isinstance(fallback_id, str) and fallback_id.strip():
        match = re.match(r"^[a-z]+-(\d{4})(\d{2})(\d{2})-", fallback_id.strip())
        if match:
            year, month, day = match.groups()
            return f"{year}-{month}-{day}"
    return ""


def extract_display_date(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        return ""

    raw = value.strip()
    normalized = raw.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized).date().isoformat()
    except ValueError:
        return ""


def subject_from_identifier(identifier: str) -> str:
    trimmed = identifier.strip()
    match = re.match(r"^[a-z]+-\d{8}-(.+?)-\d+$", trimmed)
    slug = match.group(1) if match else trimmed
    tokens = [token for token in slug.split("-") if token]
    if not tokens:
        return trimmed
    return " ".join(humanize_token(token) for token in tokens)


def humanize_token(token: str) -> str:
    lowered = token.lower()
    if lowered in _ACRONYM_TOKENS:
        return _ACRONYM_TOKENS[lowered]
    if token.isupper():
        return token
    return token[0].upper() + token[1:]
