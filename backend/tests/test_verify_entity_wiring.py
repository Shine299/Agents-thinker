"""SPEC-02 Escenario 4: verify_entity must actually be reachable from a turn,
not just exist as an untouched pure function. Covers both the stub agent
(detects a verifiable entity in the free-text message) and the real agent
(the model has the tool available under the contract's name).
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ["VENTANA_AGENT_BACKEND"] = "stub"

from contracts import Page, PageElement, TurnRequest
from agent import run_turn, build_agent_tools
from session_store import get_session
from tools import TurnContext


def page_with_company_field():
    return Page(
        url="http://x",
        title="t",
        elements=[
            PageElement(ref="e0", tag="input", type="text", label="Razon social de la empresa", value=""),
            PageElement(ref="e1", tag="input", type="text", label="RUC de la empresa", value=""),
        ],
    )


def test_stub_agent_calls_verify_entity_when_the_message_names_a_company():
    request = TurnRequest(
        session_id="s_verify_company",
        locale="es",
        message="Solicitud de GRUPO ANDINO SAC con RUC 20456789123.",
        page=page_with_company_field(),
        action_results=None,
    )

    response = run_turn(request)

    assert any(step.tool == "verify_entity" for step in response.trace)


def test_verify_entity_trace_step_comes_before_the_fill_field_it_supports():
    request = TurnRequest(
        session_id="s_verify_order",
        locale="es",
        message="Solicitud de GRUPO ANDINO SAC con RUC 20456789123.",
        page=page_with_company_field(),
        action_results=None,
    )

    response = run_turn(request)

    tools_in_order = [step.tool for step in response.trace]
    assert "verify_entity" in tools_in_order
    assert "fill_field" in tools_in_order
    assert tools_in_order.index("verify_entity") < tools_in_order.index("fill_field")


def test_stub_agent_does_not_call_verify_entity_when_nothing_verifiable_is_mentioned():
    request = TurnRequest(
        session_id="s_verify_none",
        locale="es",
        message="Solo quiero llenar mi nombre.",
        page=Page(
            url="http://x",
            title="t",
            elements=[PageElement(ref="e0", tag="input", type="text", label="Nombre del solicitante", value="")],
        ),
        action_results=None,
    )

    response = run_turn(request)

    assert not any(step.tool == "verify_entity" for step in response.trace)


def test_build_agent_tools_now_returns_three_callables_including_verify_entity():
    ctx = TurnContext(page=page_with_company_field(), locale="es")
    session = get_session("s_verify_real_tools")

    tools = build_agent_tools(ctx, session)

    assert len(tools) == 3
    verify_tool = tools[2]
    result = verify_tool(query="GRUPO ANDINO SAC")
    assert isinstance(result, str)
