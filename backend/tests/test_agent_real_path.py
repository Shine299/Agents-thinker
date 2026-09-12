"""Tests for the real (non-stub) agent path.

These cover the wiring that Sprint-01's first pass left untested: that the
tools the OpenAI Agents SDK calls actually record their proposals into the
turn context, and that the active locale reaches the model's instructions.
They exercise the real code path without any network call, by driving the
plain callables the SDK wraps.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from agent import build_agent_tools, build_instructions
from contracts import Page, PageElement
from session_store import get_session
from tools import RefNotFoundError, TurnContext, fill_field, read_page


def make_page() -> Page:
    return Page(
        url="http://localhost:5500/mesa-partes.html",
        title="Registro de solicitud",
        elements=[
            PageElement(ref="e0", tag="input", type="text", label="Nombre del solicitante", value=""),
            PageElement(ref="e1", tag="input", type="text", label="RUC de la empresa", value=""),
        ],
    )


def test_fill_field_appends_the_proposed_action_to_the_context():
    ctx = TurnContext(page=make_page(), locale="es")

    fill_field(ctx, ref="e0", value="Juan Perez Quispe", reason="Campo «Nombre del solicitante»")

    assert len(ctx.actions) == 1
    assert ctx.actions[0].args == {"ref": "e0", "value": "Juan Perez Quispe"}
    assert ctx.actions[0].needs_approval is True


def test_fill_field_assigns_sequential_action_ids():
    ctx = TurnContext(page=make_page(), locale="es")

    fill_field(ctx, ref="e0", value="Juan", reason="r1")
    fill_field(ctx, ref="e1", value="20456789123", reason="r2")

    assert [a.action_id for a in ctx.actions] == ["a1", "a2"]


def test_fill_field_raises_ref_not_found_and_records_it_in_the_trace():
    ctx = TurnContext(page=make_page(), locale="es")

    with pytest.raises(RefNotFoundError):
        fill_field(ctx, ref="e99", value="x", reason="r")

    assert ctx.actions == []
    assert any("ref_not_found" in step.outcome for step in ctx.trace)


def test_read_page_records_a_trace_step():
    ctx = TurnContext(page=make_page(), locale="es")

    read_page(ctx)

    assert len(ctx.trace) == 1
    assert ctx.trace[0].tool == "read_page"


def test_real_agent_fill_field_tool_records_into_the_context():
    """The bug this locks down: the SDK-facing tool used to discard its result,
    so the real path always returned zero actions.
    """
    ctx = TurnContext(page=make_page(), locale="es")
    _read_page_tool, fill_field_tool, _verify_entity_tool = build_agent_tools(ctx, get_session(f"s_test_{id(ctx)}"))

    result = fill_field_tool(ref="e0", value="Juan Perez Quispe", reason="Campo «Nombre del solicitante»")

    assert result == "ok"
    assert len(ctx.actions) == 1


def test_real_agent_fill_field_tool_returns_ref_not_found_without_raising():
    ctx = TurnContext(page=make_page(), locale="es")
    _read_page_tool, fill_field_tool, _verify_entity_tool = build_agent_tools(ctx, get_session(f"s_test_{id(ctx)}"))

    result = fill_field_tool(ref="e99", value="x", reason="r")

    assert result == "ref_not_found"
    assert ctx.actions == []


@pytest.mark.parametrize("locale", ["es", "en"])
def test_instructions_carry_the_active_locale_to_the_model(locale):
    instructions = build_instructions(locale)

    assert locale in instructions


def test_real_agent_builds_with_the_contract_tool_names():
    """Locks down two failures that stayed invisible while only the stub ran:
    the SDK not importing at all on this interpreter, and the model being shown
    Python identifiers instead of the frozen contract's tool names.
    """
    from agents import Agent, function_tool

    from agent import build_instructions

    ctx = TurnContext(page=make_page(), locale="es")
    read_page_tool, fill_field_tool, verify_entity_tool = build_agent_tools(ctx, get_session(f"s_test_{id(ctx)}"))

    agent = Agent(
        name="ventana",
        instructions=build_instructions(ctx.locale),
        tools=[
            function_tool(read_page_tool, name_override="read_page"),
            function_tool(fill_field_tool, name_override="fill_field"),
            function_tool(verify_entity_tool, name_override="verify_entity"),
        ],
    )

    assert [tool.name for tool in agent.tools] == ["read_page", "fill_field", "verify_entity"]


def test_no_submit_tool_is_exposed_to_the_model():
    ctx = TurnContext(page=make_page(), locale="es")

    tools = build_agent_tools(ctx, get_session(f"s_test_{id(ctx)}"))

    assert len(tools) == 3


def test_openrouter_is_used_as_the_backup_route_when_openai_key_is_absent(monkeypatch):
    """docs/RIESGOS.md R8: same call format, zero refactor."""
    from agent import configure_model_client

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")

    assert configure_model_client() == "openrouter"


def test_openai_wins_when_both_keys_are_present(monkeypatch):
    from agent import configure_model_client

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")

    assert configure_model_client() == "openai"


def test_read_page_tool_shows_the_model_every_ref_and_label():
    """Found with the real key (Sprint-02 close): the tool answered
    "4 elements available" and the model invented refs like `contact_name`.
    The model can only cite refs it has actually been shown.
    """
    ctx = TurnContext(page=make_page(), locale="es")
    read_page_tool, _, _ = build_agent_tools(ctx, get_session("s_read_page_tool"))

    shown = read_page_tool()

    for element in make_page().elements:
        assert element.ref in shown
        assert element.label in shown


def test_turn_input_carries_the_page_index_and_the_user_message():
    """With the real key the model skipped read_page and proposed invented refs
    on its first call. The index must be in the turn input from the start —
    the system prompt already promises "the page.elements index you are given".
    """
    from agent import build_turn_input

    ctx = TurnContext(page=make_page(), locale="es")
    text = build_turn_input(ctx, "Solicitud de Juan Perez Quispe")

    assert "Solicitud de Juan Perez Quispe" in text
    for element in make_page().elements:
        assert element.ref in text
        assert element.label in text
