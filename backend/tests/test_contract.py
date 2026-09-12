"""Sprint-01 contract tests, one per SPEC-01 scenario. Run with
VENTANA_AGENT_BACKEND=stub to certify Verde without a live API key.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# SPEC-01 Escenario 2 runs against the mock contract, not a live model call.
os.environ["VENTANA_AGENT_BACKEND"] = "stub"

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200


def test_agent_turn_returns_awaiting_approval_with_reason_and_trace():
    payload = load_fixture("mock_turn_request.json")
    response = client.post("/agent/turn", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "awaiting_approval"
    assert len(body["actions"]) >= 1
    for action in body["actions"]:
        assert action["reason"]
    assert len(body["trace"]) >= 1


def test_agent_turn_requires_locale():
    payload = load_fixture("mock_turn_request.json")
    del payload["locale"]

    response = client.post("/agent/turn", json=payload)

    assert response.status_code == 422


def test_agent_turn_responds_in_english_when_locale_is_en():
    payload = load_fixture("mock_turn_request.json")
    payload["locale"] = "en"

    response = client.post("/agent/turn", json=payload)

    body = response.json()
    assert "found" in body["reply"].lower()
    assert "encontr" not in body["reply"].lower()


def test_agent_turn_responds_in_spanish_when_locale_is_es():
    payload = load_fixture("mock_turn_request.json")
    payload["locale"] = "es"

    response = client.post("/agent/turn", json=payload)

    body = response.json()
    assert "encontr" in body["reply"].lower()
    assert "found" not in body["reply"].lower()
