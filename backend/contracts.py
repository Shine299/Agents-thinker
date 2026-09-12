"""Pydantic models mirroring docs/API_CONTRACTS.md. This is the frozen
contract: field names and shapes must match it exactly, snake_case throughout.
"""

from typing import Literal, Optional

from pydantic import BaseModel


class PageElement(BaseModel):
    ref: str
    tag: str
    type: Optional[str] = None
    label: str
    value: Optional[str] = None
    options: Optional[list[dict]] = None
    required: bool = False


class Page(BaseModel):
    url: str
    title: str
    elements: list[PageElement]


class ActionResult(BaseModel):
    action_id: str
    ok: bool
    value: Optional[str] = None
    error: Optional[str] = None


class TurnRequest(BaseModel):
    session_id: str
    locale: Literal["es", "en"]
    message: Optional[str] = None
    page: Optional[Page] = None
    action_results: Optional[list[ActionResult]] = None


class Action(BaseModel):
    action_id: str
    tool: str
    args: dict
    needs_approval: bool
    reason: str


class TraceStep(BaseModel):
    step: int
    tool: str
    outcome: str


class VerifyEntityResult(BaseModel):
    found: bool
    summary: str
    source: Optional[str] = None


class TurnResponse(BaseModel):
    session_id: str
    status: Literal["awaiting_approval", "done", "error"]
    reply: str
    actions: list[Action]
    trace: list[TraceStep]
