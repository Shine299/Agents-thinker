"""Error-path tests.

docs/API_CONTRACTS.md: on failure the backend answers with a TurnResponse whose
status is "error" and whose reply is readable — never an HTTP error envelope,
never a raw error code shown to the user (docs/I18N_POLICY.md section 4).
"""

import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ["VENTANA_AGENT_BACKEND"] = "stub"

import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)

FIXTURES = Path(__file__).parent / "fixtures"

RAW_ERROR_CODES = ["ref_not_found", "element_not_visible", "page_stale", "tool_timeout", "model_error"]


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


def test_turn_timeout_returns_a_turn_response_not_an_http_error(monkeypatch):
    def slow_turn(_request):
        import time

        time.sleep(0.5)

    monkeypatch.setattr(main, "run_turn", slow_turn)
    monkeypatch.setattr(main, "TURN_TIMEOUT_SECONDS", 0.05)

    payload = load_fixture("mock_turn_request.json")
    response = client.post("/agent/turn", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "error"
    assert body["session_id"] == payload["session_id"]
    assert isinstance(body["actions"], list)
    assert isinstance(body["trace"], list)


def test_turn_timeout_reply_is_readable_and_localized(monkeypatch):
    def slow_turn(_request):
        import time

        time.sleep(0.5)

    monkeypatch.setattr(main, "run_turn", slow_turn)
    monkeypatch.setattr(main, "TURN_TIMEOUT_SECONDS", 0.05)

    payload = load_fixture("mock_turn_request.json")
    payload["locale"] = "en"
    reply_en = client.post("/agent/turn", json=payload).json()["reply"]

    payload["locale"] = "es"
    reply_es = client.post("/agent/turn", json=payload).json()["reply"]

    assert reply_en != reply_es
    for code in RAW_ERROR_CODES:
        assert code not in reply_en
        assert code not in reply_es


def test_missing_page_reply_never_leaks_a_raw_error_code():
    payload = load_fixture("mock_turn_request.json")
    payload["page"] = None

    body = client.post("/agent/turn", json=payload).json()

    assert body["status"] == "error"
    for code in RAW_ERROR_CODES:
        assert code not in body["reply"]


def test_missing_page_keeps_the_technical_detail_in_the_trace():
    """The user sees plain language; the technical detail stays in the trace."""
    payload = load_fixture("mock_turn_request.json")
    payload["page"] = None

    body = client.post("/agent/turn", json=payload).json()

    assert len(body["trace"]) >= 1
