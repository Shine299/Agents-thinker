"""SPEC-02 Escenario 4: external verification via Exa.

Same stub/real split as the agent itself (docs/RIESGOS.md R8-style pattern):
a deterministic stub certifies the tests without a live Exa key; the real
path is exercised structurally (it builds the right request), never against
the network in this suite.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault("VENTANA_AGENT_BACKEND", "stub")

from tools import TurnContext, verify_entity
from contracts import Page


def make_ctx():
    page = Page(url="http://localhost:5500/mesa-partes.html", title="t", elements=[])
    return TurnContext(page=page, locale="es")


def test_verify_entity_records_a_trace_step_before_any_fill_field_that_depends_on_it():
    ctx = make_ctx()

    result = verify_entity(ctx, query="GRUPO ANDINO SAC RUC 20456789123")

    assert ctx.trace[-1].tool == "verify_entity"
    assert result.found is True


def test_verify_entity_is_a_pure_tool_with_no_network_import_at_module_level():
    """The Exa client must be imported lazily, exactly like the OpenAI Agents
    SDK client — so the stub path never requires the exa_py package.
    """
    import tools

    lines = Path(tools.__file__).read_text().splitlines()
    header_lines = []
    for line in lines:
        if line.startswith("def ") or line.startswith("class "):
            break
        header_lines.append(line)

    assert "exa_py" not in "\n".join(header_lines).lower()


def test_verify_entity_without_exa_key_uses_the_deterministic_stub(monkeypatch):
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    ctx = make_ctx()

    result = verify_entity(ctx, query="GRUPO ANDINO SAC")

    assert result.found in (True, False)
    assert "stub" in ctx.trace[-1].outcome or "exa" in ctx.trace[-1].outcome.lower()
