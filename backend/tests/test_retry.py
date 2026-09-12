"""SPEC-02 Escenario 3: retry once on ref_not_found, never in a loop.

The retry spans two HTTP turns: turn 1 proposes fill_field against page v1;
the content script executes it and the ref may no longer exist (page
changed); turn 2 carries the failure back in action_results plus a freshly
re-read page. The backend must re-locate the same conceptual field by its
original label and retry exactly once — never a second time, and always
still needs_approval.

Each test uses its own session_id: session state lives in a module-level
dict (in-memory per session_id, per docs/TECH_STACK.md), so sharing a
session_id across tests would leak state from one test into another.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os

os.environ["VENTANA_AGENT_BACKEND"] = "stub"

from contracts import ActionResult, Page, PageElement, TurnRequest
from agent import run_turn


def page_v1():
    return Page(
        url="http://localhost:5500/mesa-partes.html",
        title="t",
        elements=[PageElement(ref="e0", tag="input", type="text", label="Nombre del solicitante", value="")],
    )


def page_v2_same_field_new_ref():
    """The field is still there, but the DOM changed and it got reindexed
    under a different ref — the realistic ref_not_found case.
    """
    return Page(
        url="http://localhost:5500/mesa-partes.html",
        title="t",
        elements=[PageElement(ref="e7", tag="input", type="text", label="Nombre del solicitante", value="")],
    )


def page_v3_field_gone():
    return Page(url="http://localhost:5500/mesa-partes.html", title="t", elements=[])


def propose(session_id, locale="es"):
    request = TurnRequest(
        session_id=session_id,
        locale=locale,
        message="llena el nombre" if locale == "es" else "fill the name",
        page=page_v1(),
        action_results=None,
    )
    return run_turn(request)


def test_first_turn_proposes_the_field_against_e0():
    response = propose("s_retry_basic")
    assert response.status == "awaiting_approval"
    assert response.actions[0].args["ref"] == "e0"


def test_retry_relocates_the_field_by_label_and_proposes_it_again():
    session_id = "s_retry_relocate"
    first = propose(session_id)
    original_action_id = first.actions[0].action_id

    retry_request = TurnRequest(
        session_id=session_id,
        locale="es",
        message=None,
        page=page_v2_same_field_new_ref(),
        action_results=[ActionResult(action_id=original_action_id, ok=False, error="ref_not_found")],
    )
    retried = run_turn(retry_request)

    assert retried.status == "awaiting_approval"
    assert len(retried.actions) == 1
    assert retried.actions[0].args["ref"] == "e7"
    assert retried.actions[0].needs_approval is True


def test_retry_is_visible_in_the_trace():
    session_id = "s_retry_trace"
    first = propose(session_id)
    original_action_id = first.actions[0].action_id

    retry_request = TurnRequest(
        session_id=session_id,
        locale="es",
        message=None,
        page=page_v2_same_field_new_ref(),
        action_results=[ActionResult(action_id=original_action_id, ok=False, error="ref_not_found")],
    )
    retried = run_turn(retry_request)

    assert any("retry" in step.tool or "ref_not_found" in step.outcome for step in retried.trace)


def test_second_failure_stops_and_reports_never_loops():
    """One retry only. If the field is genuinely gone, stop and tell the
    user in plain language — no second retry attempt.
    """
    session_id = "s_retry_exhausted"

    first = propose(session_id)
    original_action_id = first.actions[0].action_id

    retried = run_turn(
        TurnRequest(
            session_id=session_id,
            locale="es",
            message=None,
            page=page_v2_same_field_new_ref(),
            action_results=[ActionResult(action_id=original_action_id, ok=False, error="ref_not_found")],
        )
    )
    retried_action_id = retried.actions[0].action_id

    exhausted = run_turn(
        TurnRequest(
            session_id=session_id,
            locale="es",
            message=None,
            page=page_v3_field_gone(),
            action_results=[ActionResult(action_id=retried_action_id, ok=False, error="ref_not_found")],
        )
    )

    assert exhausted.actions == []
    assert exhausted.status == "done"
    assert "ref_not_found" not in exhausted.reply
    assert any("ref_not_found" in step.outcome for step in exhausted.trace)


def test_successful_action_result_needs_no_retry_and_is_not_reproposed():
    session_id = "s_retry_success"

    first = propose(session_id)
    action_id = first.actions[0].action_id

    resolved = run_turn(
        TurnRequest(
            session_id=session_id,
            locale="es",
            message=None,
            page=page_v1(),
            action_results=[ActionResult(action_id=action_id, ok=True, value="Juan Perez Quispe", error=None)],
        )
    )

    assert resolved.actions == []
    assert resolved.status == "done"


def test_retry_reply_never_leaks_the_raw_error_code_in_any_locale():
    for locale in ("es", "en"):
        session_id = f"s_retry_exhausted_{locale}"
        first = propose(session_id, locale=locale)
        original_action_id = first.actions[0].action_id

        retried = run_turn(
            TurnRequest(
                session_id=session_id,
                locale=locale,
                message=None,
                page=page_v2_same_field_new_ref(),
                action_results=[ActionResult(action_id=original_action_id, ok=False, error="ref_not_found")],
            )
        )
        retried_action_id = retried.actions[0].action_id

        exhausted = run_turn(
            TurnRequest(
                session_id=session_id,
                locale=locale,
                message=None,
                page=page_v3_field_gone(),
                action_results=[ActionResult(action_id=retried_action_id, ok=False, error="ref_not_found")],
            )
        )
        assert "ref_not_found" not in exhausted.reply
