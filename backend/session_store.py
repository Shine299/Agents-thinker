"""In-memory session state, one dict per session_id (docs/TECH_STACK.md — no
database; the history lives only while the process runs).

This is what makes the retry-once rule (docs/API_CONTRACTS.md, "un solo
reintento por acción, nunca en bucle") possible across two HTTP turns: a ref
is not stable once the DOM changes, but we remember which label each
action_id was proposed for, so turn 2 can re-locate the field and retry
exactly once.
"""

from dataclasses import dataclass, field


@dataclass
class ProposedField:
    label: str
    value: str


@dataclass
class SessionState:
    # action_id -> what it was proposed for, so a failure can be retried by label.
    proposed: dict = field(default_factory=dict)
    # labels already retried once — never retried a second time.
    retried_labels: set = field(default_factory=set)


_SESSIONS: dict[str, SessionState] = {}


def get_session(session_id: str) -> SessionState:
    if session_id not in _SESSIONS:
        _SESSIONS[session_id] = SessionState()
    return _SESSIONS[session_id]


def reset_all():
    """Test-only escape hatch — production never needs to clear this."""
    _SESSIONS.clear()
