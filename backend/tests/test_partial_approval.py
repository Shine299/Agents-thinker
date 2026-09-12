"""SPEC-02 Escenario 2, the part the first pass got wrong: approving only
some of N proposed actions must leave the rest visibly pending — the backend
must never say "done" while other proposed fields are still unresolved.

Also covers the "discarded" outcome: an action the user declined to approve
must be removable from session state without being treated as a failed
retry candidate or as a completed fill.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ["VENTANA_AGENT_BACKEND"] = "stub"

from contracts import ActionResult, Page, PageElement, TurnRequest
from agent import run_turn


def page_with_three_fields():
    return Page(
        url="http://x",
        title="t",
        elements=[
            PageElement(ref="e0", tag="input", type="text", label="Campo A", value=""),
            PageElement(ref="e1", tag="input", type="text", label="Campo B", value=""),
            PageElement(ref="e2", tag="input", type="text", label="Campo C", value=""),
        ],
    )


def propose_three(session_id):
    return run_turn(
        TurnRequest(session_id=session_id, locale="es", message="llena todo", page=page_with_three_fields(), action_results=None)
    )


def test_approving_one_of_three_does_not_report_done():
    session_id = "s_partial_1of3"
    first = propose_three(session_id)
    assert len(first.actions) == 3
    action_a = first.actions[0]

    resolved_one = run_turn(
        TurnRequest(
            session_id=session_id,
            locale="es",
            message=None,
            page=page_with_three_fields(),
            action_results=[ActionResult(action_id=action_a.action_id, ok=True, value="x", error=None)],
        )
    )

    assert resolved_one.status != "done", "reported done while 2 of 3 fields are still unresolved"
    assert "ref_not_found" not in resolved_one.reply


def test_status_is_done_only_once_every_proposed_action_is_resolved():
    session_id = "s_partial_all_resolved"
    first = propose_three(session_id)
    a, b, c = first.actions

    run_turn(
        TurnRequest(
            session_id=session_id, locale="es", message=None, page=page_with_three_fields(),
            action_results=[ActionResult(action_id=a.action_id, ok=True, value="x", error=None)],
        )
    )
    run_turn(
        TurnRequest(
            session_id=session_id, locale="es", message=None, page=page_with_three_fields(),
            action_results=[ActionResult(action_id=b.action_id, ok=True, value="y", error=None)],
        )
    )
    final = run_turn(
        TurnRequest(
            session_id=session_id, locale="es", message=None, page=page_with_three_fields(),
            action_results=[ActionResult(action_id=c.action_id, ok=True, value="z", error=None)],
        )
    )

    assert final.status == "done"


def test_discarded_action_is_not_retried_and_does_not_block_done():
    session_id = "s_discard_flow"
    first = propose_three(session_id)
    a, b, c = first.actions

    run_turn(
        TurnRequest(
            session_id=session_id, locale="es", message=None, page=page_with_three_fields(),
            action_results=[ActionResult(action_id=a.action_id, ok=False, value=None, error="discarded")],
        )
    )
    run_turn(
        TurnRequest(
            session_id=session_id, locale="es", message=None, page=page_with_three_fields(),
            action_results=[ActionResult(action_id=b.action_id, ok=True, value="y", error=None)],
        )
    )
    final = run_turn(
        TurnRequest(
            session_id=session_id, locale="es", message=None, page=page_with_three_fields(),
            action_results=[ActionResult(action_id=c.action_id, ok=True, value="z", error=None)],
        )
    )

    assert final.status == "done"


def test_discarded_action_id_is_not_reported_as_an_exhausted_retry():
    session_id = "s_discard_no_exhaust"
    first = propose_three(session_id)
    a = first.actions[0]

    discarded = run_turn(
        TurnRequest(
            session_id=session_id, locale="es", message=None, page=page_with_three_fields(),
            action_results=[ActionResult(action_id=a.action_id, ok=False, value=None, error="discarded")],
        )
    )

    assert "Campo A" not in discarded.reply
