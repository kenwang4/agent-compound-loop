"""Pytest coverage for writeback_candidate CLI / schema."""

from __future__ import annotations

import json
import uuid
from argparse import Namespace
from pathlib import Path

import pytest

from writeback_candidate import __version__
from writeback_candidate.cli import (
    SCHEMA,
    _safe_ref,
    _validate_candidate,
    create_candidate,
)

REPO = Path(__file__).resolve().parent.parent


def test_schema_load():
    """Schema file exists, is valid JSON, and declares expected required fields."""
    assert SCHEMA.is_file(), f"missing schema at {SCHEMA}"
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert data.get("title") == "Writeback Candidate"
    assert data.get("type") == "object"
    required = set(data.get("required") or [])
    for field in (
        "schema_version",
        "candidate_id",
        "lane",
        "claim",
        "source",
        "destination",
        "status",
        "task_id",
    ):
        assert field in required
    assert data["properties"]["schema_version"]["const"] == "1.0"
    assert __version__ == "0.1.0"
    # Status / lane enums must stay tight so CI / reviewers share one vocabulary
    status_enum = set(data["properties"]["status"]["enum"])
    assert status_enum == {
        "pending",
        "in_review",
        "accepted_pending_writeback",
        "rejected",
        "superseded",
        "expired",
    }
    assert data["properties"]["lane"]["enum"] == ["fast", "durable"]


def test_reject_absolute_users_path():
    """Absolute /Users/... refs must be rejected (privacy / portability)."""
    with pytest.raises(ValueError, match="relative"):
        _safe_ref("/Users/demo/secret/notes.md", "source")
    with pytest.raises(ValueError, match="relative"):
        _safe_ref("/Users/someone/anything", "destination")
    with pytest.raises(ValueError, match="relative"):
        _safe_ref("~/private/file.md", "artifact")
    # Relative refs remain OK
    assert _safe_ref("docs/04-minigame-gates.md", "destination") == "docs/04-minigame-gates.md"


def test_happy_path_candidate_create():
    """Durable create writes a candidate JSON under writeback_candidates/."""
    inbox = REPO / "writeback_candidates"
    inbox.mkdir(parents=True, exist_ok=True)
    candidate_id = f"test_{uuid.uuid4().hex[:10]}"
    out_path = inbox / f"candidate_{candidate_id}.json"

    if out_path.exists():
        out_path.unlink()

    args = Namespace(
        lane="durable",
        claim="Test claim: cancel timers in one cleanup entry",
        source="examples/fake-test-log.txt",
        destination="docs/04-minigame-gates.md",
        owner="maintainer",
        scope="test-scope",
        review_on="next-independent-review",
        ttl_days=30,
        acceptance="pytest happy path",
        artifact="examples/fake-test-log.txt",
        candidate_id=candidate_id,
        task_id="pytest-task-001",
        session_id="pytest-session",
    )

    try:
        rc = create_candidate(args)
        assert rc == 0
        assert out_path.is_file()
        payload = json.loads(out_path.read_text(encoding="utf-8"))
        assert payload["candidate_id"] == candidate_id
        assert payload["lane"] == "durable"
        assert payload["status"] == "pending"
        assert payload["schema_version"] == "1.0"
        _validate_candidate(payload)
        assert not payload["source"].startswith("/")
        assert "/Users/" not in payload["destination"]
    finally:
        if out_path.exists():
            out_path.unlink()


def test_create_rejects_users_path_via_cli_args():
    """create_candidate rejects absolute source before writing."""
    args = Namespace(
        lane="durable",
        claim="should never land",
        source="/Users/demo/leak.txt",
        destination="docs/01-recursive-evolution.md",
        owner="maintainer",
        scope="test",
        review_on="never",
        ttl_days=7,
        acceptance="",
        artifact="",
        candidate_id=f"reject_{uuid.uuid4().hex[:8]}",
        task_id="reject-task",
        session_id="reject-session",
    )
    with pytest.raises(ValueError, match="relative"):
        create_candidate(args)
