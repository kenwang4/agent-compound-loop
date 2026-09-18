#!/usr/bin/env python3
"""Bounded candidate inbox for the two-speed writeback flow.

Fast lane returns a session-only result. Durable lane writes a candidate JSON
for later independent review; neither lane mutates canonical assets.

Public OSS build: no host-private imports; path refs must stay relative;
default owner is ``maintainer``.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "writeback_candidates"
SCHEMA = ROOT / "schemas" / "writeback_candidate.schema.json"
MAX_PENDING = 20
MAX_BYTES = 12 * 1024
DEFAULT_TTL_DAYS = 30
REQUIRED_FIELDS = {
    "schema_version",
    "candidate_id",
    "lane",
    "claim",
    "source",
    "owner",
    "scope",
    "review_on",
    "destination",
    "status",
    "created_at",
    "expires_at",
    "task_id",
}
ALLOWED_STATUSES = {
    "pending",
    "in_review",
    "accepted_pending_writeback",
    "rejected",
    "superseded",
    "expired",
}

# Lightweight secret / PII heuristics for public use (not a full scanner).
_BLOCK_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]"),
    re.compile(r"(?i)secret\s*[:=]"),
    re.compile(r"(?i)bearer\s+[a-z0-9\-._~+/]+=*"),
    re.compile(r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b"),  # any email
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _candidate_files() -> list[Path]:
    INBOX.mkdir(parents=True, exist_ok=True)
    return sorted(path for path in INBOX.glob("candidate_*.json") if path.is_file())


def _pending_count() -> int:
    count = 0
    for path in _candidate_files():
        try:
            status = json.loads(path.read_text(encoding="utf-8")).get("status")
        except (OSError, json.JSONDecodeError):
            status = "pending"
        if status in {"pending", "in_review", "accepted_pending_writeback"}:
            count += 1
    return count


def _parse_timestamp(value: Any) -> datetime:
    text = str(value or "").replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _expire_candidates(now: datetime | None = None) -> int:
    """Mark overdue open candidates expired whenever the inbox is touched."""
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    expired = 0
    for path in _candidate_files():
        try:
            candidate = json.loads(path.read_text(encoding="utf-8"))
            if (
                candidate.get("status")
                in {"pending", "in_review", "accepted_pending_writeback"}
                and _parse_timestamp(candidate.get("expires_at")) <= current
            ):
                candidate["status"] = "expired"
                candidate["reviewer"] = "system:ttl"
                candidate["review_evidence"] = "writeback_candidate.py:ttl"
                candidate["reviewed_at"] = current.isoformat(timespec="seconds")
                _validate_candidate(candidate)
                path.write_text(
                    json.dumps(candidate, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                expired += 1
        except (OSError, ValueError, json.JSONDecodeError):
            continue
    return expired


def _safe_ref(value: str, field: str) -> str:
    value = str(value or "").strip()
    if not value:
        raise ValueError(f"{field} is required")
    if len(value) > 500:
        raise ValueError(f"{field} exceeds 500 characters")
    # Reject absolute / home / machine-specific paths (POSIX, Windows drive, UNC).
    if (
        value.startswith("/")
        or value.startswith("~")
        or "/Users/" in value
        or "/home/" in value
    ):
        raise ValueError(f"{field} must use a relative, non-machine-specific reference")
    if re.match(r"^[A-Za-z]:[\\/]", value) or value.startswith("\\\\") or value.startswith("//"):
        raise ValueError(f"{field} must use a relative, non-machine-specific reference")
    return value


def _clean_text(value: str, field: str, limit: int) -> str:
    value = str(value or "").strip()
    if not value:
        raise ValueError(f"{field} is required")
    if len(value) > limit:
        raise ValueError(f"{field} exceeds {limit} characters")
    return value


def _scan_candidate(candidate: dict[str, Any]) -> None:
    fields = " ".join(
        str(candidate.get(key, ""))
        for key in ("claim", "source", "verified_by", "scope", "destination", "acceptance")
    )
    for pattern in _BLOCK_PATTERNS:
        if pattern.search(fields):
            raise ValueError(f"candidate blocked by privacy/secret heuristic: {pattern.pattern}")


def _validate_candidate(candidate: dict[str, Any]) -> None:
    missing = REQUIRED_FIELDS.difference(candidate)
    if missing:
        raise ValueError(f"candidate missing required fields: {sorted(missing)}")
    if candidate.get("schema_version") != "1.0" or candidate.get("lane") != "durable":
        raise ValueError("unsupported candidate schema or lane")
    if candidate.get("status") not in ALLOWED_STATUSES:
        raise ValueError("invalid candidate status")
    try:
        expires_at = _parse_timestamp(candidate.get("expires_at"))
    except (TypeError, ValueError):
        raise ValueError("expires_at must be an ISO-8601 timestamp") from None
    if (
        candidate.get("status") != "expired"
        and expires_at <= _parse_timestamp(candidate["created_at"])
    ):
        raise ValueError("expires_at must be after created_at")
    for field in ("source", "destination", "artifact", "review_evidence"):
        value = candidate.get(field) or ""
        if value:
            _safe_ref(value, field)
    _scan_candidate(candidate)
    encoded = (json.dumps(candidate, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if len(encoded) > MAX_BYTES:
        raise ValueError(f"candidate exceeds {MAX_BYTES} bytes")


def _stable_task_id(explicit: str, claim: str) -> str:
    if explicit.strip():
        return _clean_text(explicit, "task_id", 160)
    return f"task_{uuid.uuid5(uuid.NAMESPACE_URL, claim).hex[:16]}"


def create_candidate(args: argparse.Namespace) -> int:
    _expire_candidates()
    if args.lane == "fast":
        print(
            json.dumps(
                {
                    "status": "session_only",
                    "lane": "fast",
                    "writeback": False,
                    "reason": "fast lane does not create durable candidates",
                },
                ensure_ascii=False,
            )
        )
        return 0
    if getattr(args, "ttl_days", DEFAULT_TTL_DAYS) < 1:
        raise ValueError("ttl-days must be at least 1")

    if _pending_count() >= MAX_PENDING:
        print(
            json.dumps(
                {
                    "status": "rejected",
                    "reason": f"candidate inbox is full ({MAX_PENDING} pending/in_review)",
                },
                ensure_ascii=False,
            )
        )
        return 2

    claim = _clean_text(args.claim, "claim", 2000)
    source = _safe_ref(args.source, "source")
    destination = _safe_ref(args.destination, "destination")
    artifact = _safe_ref(args.artifact or destination, "artifact")
    candidate_id = args.candidate_id or (
        f"{datetime.now(timezone.utc).strftime('%Y%m%d')}_{uuid.uuid4().hex[:10]}"
    )
    candidate = {
        "schema_version": "1.0",
        "candidate_id": _clean_text(candidate_id, "candidate_id", 160),
        "lane": "durable",
        "claim": claim,
        "source": source,
        "verified_by": "",
        "owner": _clean_text(args.owner, "owner", 160),
        "scope": _clean_text(args.scope, "scope", 500),
        "review_on": _clean_text(args.review_on, "review_on", 300),
        "destination": destination,
        "status": "pending",
        "reviewer": "",
        "review_evidence": "",
        "created_at": _now(),
        "expires_at": (
            datetime.now(timezone.utc)
            + timedelta(days=getattr(args, "ttl_days", DEFAULT_TTL_DAYS))
        ).isoformat(timespec="seconds"),
        "reviewed_at": None,
        "task_id": _stable_task_id(args.task_id or "", claim),
        "session_id": (args.session_id or "session_local")[:160],
        "artifact": artifact,
        "acceptance": (args.acceptance or "")[:2000],
    }
    _validate_candidate(candidate)
    encoded = (json.dumps(candidate, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path = INBOX / f"candidate_{candidate['candidate_id']}.json"
    if path.exists():
        raise ValueError(f"candidate already exists: {candidate['candidate_id']}")
    path.write_bytes(encoded)
    try:
        display_path = str(path.relative_to(ROOT))
    except ValueError:
        display_path = path.name
    print(
        json.dumps(
            {
                "status": "candidate_created",
                "lane": "durable",
                "candidate_id": candidate["candidate_id"],
                "path": display_path,
                "reviewer_required": True,
                "canonical_writeback": False,
            },
            ensure_ascii=False,
        )
    )
    return 0


def review_candidate(args: argparse.Namespace) -> int:
    _expire_candidates()
    matches = [
        path
        for path in _candidate_files()
        if path.stem == f"candidate_{args.candidate_id}"
    ]
    if not matches:
        print(
            json.dumps(
                {"status": "not_found", "candidate_id": args.candidate_id},
                ensure_ascii=False,
            )
        )
        return 1
    path = matches[0]
    candidate = json.loads(path.read_text(encoding="utf-8"))
    if candidate.get("status") == "expired":
        print(
            json.dumps(
                {
                    "status": "expired",
                    "candidate_id": args.candidate_id,
                    "canonical_writeback": False,
                },
                ensure_ascii=False,
            )
        )
        return 2
    candidate["status"] = (
        "accepted_pending_writeback" if args.verdict == "accepted" else args.verdict
    )
    candidate["reviewer"] = _clean_text(args.reviewer, "reviewer", 160)
    candidate["verified_by"] = candidate["reviewer"]
    candidate["review_evidence"] = _safe_ref(args.evidence, "evidence")
    candidate["reviewed_at"] = _now()
    _validate_candidate(candidate)
    path.write_text(
        json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "review_recorded",
                "candidate_id": args.candidate_id,
                "verdict": candidate["status"],
                "canonical_writeback": False,
            },
            ensure_ascii=False,
        )
    )
    return 0


def list_candidates(_: argparse.Namespace) -> int:
    expired = _expire_candidates()
    rows = []
    for path in _candidate_files():
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
            rows.append(
                {
                    "candidate_id": item.get("candidate_id"),
                    "status": item.get("status"),
                    "lane": item.get("lane"),
                    "task_id": item.get("task_id"),
                    "destination": item.get("destination"),
                }
            )
        except (OSError, json.JSONDecodeError) as exc:
            try:
                rel = str(path.relative_to(ROOT))
            except ValueError:
                rel = path.name
            rows.append({"path": rel, "status": "invalid", "error": str(exc)})
    print(
        json.dumps(
            {
                "pending": _pending_count(),
                "expired_now": expired,
                "max_pending": MAX_PENDING,
                "items": rows,
            },
            ensure_ascii=False,
        )
    )
    return 0


def main() -> int:
    from writeback_candidate import __version__

    parser = argparse.ArgumentParser(
        description="Manage bounded durable writeback candidates"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--lane", choices=("fast", "durable"), default="fast")
    create.add_argument("--claim", required=True)
    create.add_argument("--source", default="session-evidence")
    create.add_argument("--owner", default="maintainer")
    create.add_argument("--scope", default="current-task")
    create.add_argument("--review-on", default="next-independent-review")
    create.add_argument("--ttl-days", type=int, default=DEFAULT_TTL_DAYS)
    create.add_argument("--destination", default="docs/02-writeback-protocol.md")
    create.add_argument("--acceptance", default="")
    create.add_argument("--artifact", default="")
    create.add_argument("--candidate-id", default="")
    create.add_argument("--task-id", default="")
    create.add_argument("--session-id", default="")
    create.set_defaults(func=create_candidate)

    review = sub.add_parser("review")
    review.add_argument("--candidate-id", required=True)
    review.add_argument("--verdict", choices=("accepted", "rejected"), required=True)
    review.add_argument("--reviewer", required=True)
    review.add_argument("--evidence", required=True)
    review.set_defaults(func=review_candidate)

    listing = sub.add_parser("list")
    listing.set_defaults(func=list_candidates)

    args = parser.parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "rejected", "reason": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
