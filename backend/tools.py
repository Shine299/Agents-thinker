"""Pure domain tools. No FastAPI, no extension details — only the shapes
defined in contracts.py. See docs/ARCHITECTURE.md, "dependency rule".

read_page and fill_field never touch any DOM — they record a proposed
action with needs_approval=True; the content script executes it after human
approval. extract_table stays out of scope (Flujo 2, explicitly deferred in
MEMORY.md).

Every tool writes its result into the TurnContext it is given. That is what
keeps the stub path and the real agent path from drifting apart: both call
these same functions, so a proposal can never be silently dropped.
"""

import os
from typing import Optional

from contracts import Action, Page, PageElement, TraceStep, VerifyEntityResult

REF_NOT_FOUND = "ref_not_found"


class RefNotFoundError(Exception):
    """Raised when a ref is no longer present in the page index."""

    def __init__(self, ref: str):
        super().__init__(REF_NOT_FOUND)
        self.ref = ref


class TurnContext:
    """Mutable per-turn state. Tools append their proposals and trace steps
    here; the caller reads them back once the loop is done.
    """

    def __init__(self, page: Page, locale: str):
        self.page = page
        self.locale = locale
        self.actions: list[Action] = []
        self.trace: list[TraceStep] = []

    def record(self, tool: str, outcome: str) -> TraceStep:
        step = TraceStep(step=len(self.trace) + 1, tool=tool, outcome=outcome)
        self.trace.append(step)
        return step

    def next_action_id(self) -> str:
        return f"a{len(self.actions) + 1}"


def find_element(page: Page, ref: str) -> Optional[PageElement]:
    for element in page.elements:
        if element.ref == ref:
            return element
    return None


def find_element_by_label(page: Page, label: str) -> Optional[PageElement]:
    """Used by the retry path: a ref is not stable across DOM changes, but the
    field's label usually is (docs/RIESGOS.md R3/R4 territory).
    """
    for element in page.elements:
        if element.label == label:
            return element
    return None


def read_page(ctx: TurnContext) -> Page:
    ctx.record("read_page", f"ok, {len(ctx.page.elements)} elementos")
    return ctx.page


def fill_field(ctx: TurnContext, ref: str, value: str, reason: str) -> Action:
    element = find_element(ctx.page, ref)
    if element is None:
        ctx.record("fill_field", f"{REF_NOT_FOUND} ({ref})")
        raise RefNotFoundError(ref)

    action = Action(
        action_id=ctx.next_action_id(),
        tool="fill_field",
        args={"ref": ref, "value": value},
        needs_approval=True,
        reason=reason,
    )
    ctx.actions.append(action)
    ctx.record("fill_field", f"ok, propuesta {action.action_id} sobre {ref}")
    return action


def _stub_verify_entity(query: str) -> VerifyEntityResult:
    """Deterministic, network-free result: anything that looks like a Peruvian
    RUC (11 digits) or carries a recognizable company suffix is treated as
    found. Good enough to certify the tests without an Exa key
    (docs/RIESGOS.md R8-style fallback).
    """
    import re

    looks_like_ruc = bool(re.search(r"\b\d{11}\b", query))
    looks_like_company = any(suffix in query.upper() for suffix in ("SAC", "SRL", "EIRL", "SA"))
    found = looks_like_ruc or looks_like_company
    return VerifyEntityResult(
        found=found,
        summary=f"stub: {'match' if found else 'no match'} for '{query}'",
        source=None,
    )


def _real_verify_entity(query: str) -> VerifyEntityResult:
    from exa_py import Exa

    client = Exa(api_key=os.environ["EXA_API_KEY"])
    result = client.search(query, num_results=1)
    hits = getattr(result, "results", [])
    if not hits:
        return VerifyEntityResult(found=False, summary=f"exa: no results for '{query}'", source=None)

    top = hits[0]
    return VerifyEntityResult(
        found=True,
        summary=getattr(top, "title", query),
        source=getattr(top, "url", None),
    )


def verify_entity(ctx: TurnContext, query: str) -> VerifyEntityResult:
    if os.environ.get("EXA_API_KEY"):
        result = _real_verify_entity(query)
        ctx.record("verify_entity", f"exa: {'found' if result.found else 'not found'} — {result.summary}")
    else:
        result = _stub_verify_entity(query)
        ctx.record("verify_entity", result.summary)
    return result
