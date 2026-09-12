"""Agent loop.

Real mode uses the OpenAI Agents SDK. Stub mode (see docs/RIESGOS.md R8) is a
deterministic, network-free fallback used to certify Verde before the OpenAI
credit is redeemed, and as a safety net if credit runs out mid-build.

Both modes drive the same tools from tools.py against the same TurnContext, so
neither path can quietly drop a proposal the other one keeps.

Retry-once handling (docs/API_CONTRACTS.md, "un solo reintento por acción,
nunca en bucle"): a ref is not stable once the DOM changes, so the session
store remembers which label each action_id was proposed for. When a turn
carries action_results with a ref_not_found failure, we re-locate the field
by that label in the freshly re-read page and retry exactly once.

Status/reply for a turn is never decided from this turn's new proposals
alone: session.proposed also holds every earlier proposal the user has not
yet resolved (approved, discarded, or exhausted), so approving 1 of 3 fields
never reports "done" while 2 are still waiting.
"""

import json
import os
import re

from contracts import Page, TraceStep, TurnRequest, TurnResponse
from session_store import ProposedField, SessionState, get_session
from tools import (
    RefNotFoundError,
    TurnContext,
    fill_field,
    find_element,
    find_element_by_label,
    read_page,
    verify_entity,
)

SYSTEM_PROMPT = """You operate ONLY on the page.elements index you are given — never on raw HTML.
For each field you can confidently fill from the user's message, call fill_field with the element's
ref (exactly as it appears in the index, e.g. "e3") and a proposed value, and a reason that cites the
field's exact label. Never invent a field or a ref that is not in the index. Never call any "submit"
tool — it does not exist.

If the message names a company or a tax id (RUC), call verify_entity ONCE with just that company
name and/or RUC (not the whole message) before proposing the related fields — verify_entity must
appear before the fill_field it justifies. The result is informational, not a veto: always propose
the values the user gave, and put what the lookup found (a match, a different RUC, nothing) into the
reason so the person can judge before approving. Do not ask the user to confirm first.

Be fast: issue all the fill_field calls for a page together in a single batch, not one per round.

fill_field only PROPOSES a value; nothing is written until the user approves each proposal in the
panel. Your final reply must say what you propose and that it awaits their approval — never claim
that fields were filled.

Respond in the language given by the locale stated below, no matter what language the user's
message or the page is in: "es" -> Spanish, "en" -> English. Never mix languages inside one reply.
This applies to your reply and to every reason you pass to fill_field.

Never translate: field labels (quote them verbatim, in the portal's original language), ref
identifiers, or technical error codes (ref_not_found, page_stale, etc.).
"""

# Model-written text cannot be resolved from a dictionary, so the stub and the
# error paths carry their own per-locale wording. See docs/I18N_POLICY.md #4.
REPLIES = {
    "es": "Encontré {count} campos que puedo llenar con los datos de tu mensaje.",
    "en": "I found {count} fields I can fill from your message.",
}

NOTHING_FOUND_REPLIES = {
    "es": "No encontré campos que pueda llenar con los datos de tu mensaje.",
    "en": "I found no fields I can fill from your message.",
}

STILL_PENDING_REPLIES = {
    "es": "{count} campo(s) más siguen a la espera de tu aprobación.",
    "en": "{count} more field(s) are still waiting for your approval.",
}

DONE_REPLIES = {
    "es": "Listo, los campos aprobados quedaron completados.",
    "en": "Done — the approved fields are now complete.",
}

EXHAUSTED_REPLIES = {
    "es": "No pude completar el campo «{label}» tras reintentarlo; revísalo manualmente.",
    "en": 'I could not complete the field "{label}" after retrying; please fill it in manually.',
}

REASON_TEMPLATES = {
    "es": "Campo «{label}», tomado del mensaje del usuario",
    "en": 'Field "{label}", taken from the user\'s message',
}

RETRY_REASON_TEMPLATES = {
    "es": "Campo «{label}», reintentado tras releer la página",
    "en": 'Field "{label}", retried after re-reading the page',
}

# Plain-language wording for turn-level failures. The raw technical detail
# stays in the trace; the user never reads an error code (docs/I18N_POLICY.md #4).
ERROR_REPLIES = {
    "es": {
        "missing_page": (
            "No recibí el contenido de la página. Abre el panel sobre la pestaña del portal "
            "y vuelve a intentarlo."
        ),
        "timeout": "El agente tardó demasiado en responder. No se modificó nada en la página.",
        "model_error": (
            "El agente no pudo completar la consulta. No se modificó nada en la página; "
            "puedes reintentar."
        ),
    },
    "en": {
        "missing_page": (
            "I did not receive the page content. Open the panel on the portal tab and try again."
        ),
        "timeout": "The agent took too long to respond. Nothing was changed on the page.",
        "model_error": (
            "The agent could not complete the request. Nothing was changed on the page; "
            "you can retry."
        ),
    },
}

# Heuristic for the stub agent: a Peruvian RUC (11 digits) or a name carrying
# a company suffix is treated as verifiable. Company match takes priority
# because it is more specific and reads better in verify_entity's query.
_COMPANY_PATTERN = re.compile(
    r"[A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ]*(?:\s+[A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ]*){0,4}\s+(?:SAC|SRL|EIRL|SA)\b"
)
_RUC_PATTERN = re.compile(r"\b\d{11}\b")


def _detect_verifiable_query(message: str):
    if not message:
        return None
    company_match = _COMPANY_PATTERN.search(message)
    if company_match:
        return company_match.group(0)
    ruc_match = _RUC_PATTERN.search(message)
    if ruc_match:
        return ruc_match.group(0)
    return None


def build_instructions(locale: str) -> str:
    """System prompt with the active locale bound into it, so the model is told
    which language to answer in instead of being asked to read a field it never
    receives.
    """
    return f'{SYSTEM_PROMPT}\nThe active locale for this turn is "{locale}".'


def error_response(session_id: str, locale: str, kind: str, detail: str) -> TurnResponse:
    return TurnResponse(
        session_id=session_id,
        status="error",
        reply=ERROR_REPLIES[locale][kind],
        actions=[],
        trace=[TraceStep(step=1, tool="agent_turn", outcome=detail)],
    )


def _backend_mode() -> str:
    return os.environ.get("VENTANA_AGENT_BACKEND", "openai")


def _propose(ctx: TurnContext, session: SessionState, ref: str, value: str, reason: str):
    """fill_field plus session bookkeeping: remembers which label this
    proposal was for, so a later ref_not_found can be retried by label.
    """
    action = fill_field(ctx, ref=ref, value=value, reason=reason)
    element = find_element(ctx.page, ref)
    if element is not None:
        session.proposed[action.action_id] = ProposedField(label=element.label, value=value)
    return action


def _run_stub(ctx: TurnContext, session: SessionState, message: str) -> None:
    """Deterministic mock agent: proposes filling every empty, labelled
    text-like field. No network calls. Runs verify_entity first when the
    message names something verifiable, so its trace step always precedes
    the fill_field steps it supports.
    """
    read_page(ctx)

    verifiable_query = _detect_verifiable_query(message)
    if verifiable_query:
        verify_entity(ctx, query=verifiable_query)

    fillable = [
        el
        for el in ctx.page.elements
        if el.tag in ("input", "textarea") and not el.value and el.label
    ]

    for element in fillable:
        try:
            _propose(
                ctx,
                session,
                ref=element.ref,
                value=f"<{element.label}>",
                reason=REASON_TEMPLATES[ctx.locale].format(label=element.label),
            )
        except RefNotFoundError:
            continue


def _process_action_results(ctx: TurnContext, session: SessionState, action_results) -> list:
    """Handles the second-turn contract: for each failed ref_not_found result,
    retry exactly once by relocating the field by its original label in the
    freshly re-read page. A "discarded" result (the user declined to approve
    it) is simply removed from session state — never retried, never counted
    as exhausted. Returns labels that stayed unresolved after the retry was
    exhausted, for the reply text.
    """
    exhausted_labels = []

    for result in action_results:
        proposed = session.proposed.pop(result.action_id, None)

        if result.ok or result.error == "discarded":
            continue

        if result.error != "ref_not_found" or proposed is None:
            continue

        if proposed.label in session.retried_labels:
            ctx.record(
                "fill_field",
                f"ref_not_found ({proposed.label}) — retry already used, stopping",
            )
            exhausted_labels.append(proposed.label)
            continue

        session.retried_labels.add(proposed.label)
        ctx.record("retry", f"ref_not_found — retrying once for label '{proposed.label}'")

        new_element = find_element_by_label(ctx.page, proposed.label)
        if new_element is None:
            ctx.record("fill_field", f"ref_not_found ({proposed.label}) — not found even after re-read")
            exhausted_labels.append(proposed.label)
            continue

        _propose(
            ctx,
            session,
            ref=new_element.ref,
            value=proposed.value,
            reason=RETRY_REASON_TEMPLATES[ctx.locale].format(label=proposed.label),
        )

    return exhausted_labels


def _reply_for(locale: str, ctx: TurnContext, session: SessionState, exhausted_labels, empty_reply: str) -> str:
    """Single source of truth for what the user reads. session.proposed is
    consulted, not just this turn's new actions — that is what stops a
    partial approval from ever being reported as "done".
    """
    if ctx.actions:
        return REPLIES[locale].format(count=len(ctx.actions))
    if session.proposed:
        return STILL_PENDING_REPLIES[locale].format(count=len(session.proposed))
    if exhausted_labels:
        return EXHAUSTED_REPLIES[locale].format(label=", ".join(exhausted_labels))
    return empty_reply


def _status_for(ctx: TurnContext, session: SessionState) -> str:
    return "awaiting_approval" if (ctx.actions or session.proposed) else "done"


def _index_json(page: Page) -> str:
    # The model can only cite refs it has been shown. Null/false keys are
    # dropped: same information, fewer tokens.
    return json.dumps(
        [e.model_dump(exclude_none=True, exclude_defaults=True) for e in page.elements],
        ensure_ascii=False,
    )


def build_turn_input(ctx: TurnContext, message: str) -> str:
    """The index goes in the first turn's input: with the real key the model
    skipped read_page and invented refs. read_page stays as a tool for the
    re-read after ref_not_found.
    """
    return f"page.elements index:\n{_index_json(ctx.page)}\n\nUser message:\n{message}"


def build_agent_tools(ctx: TurnContext, session: SessionState):
    """The plain callables the SDK wraps as tools. Returned unwrapped so tests
    can drive the real path's wiring without a network call.
    """

    def read_page_tool() -> str:
        return _index_json(read_page(ctx))

    def fill_field_tool(ref: str, value: str, reason: str) -> str:
        try:
            _propose(ctx, session, ref=ref, value=value, reason=reason)
            return "ok"
        except RefNotFoundError:
            return "ref_not_found"

    def verify_entity_tool(query: str) -> str:
        result = verify_entity(ctx, query=query)
        return result.summary

    return read_page_tool, fill_field_tool, verify_entity_tool


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "gpt-4o-mini"


def configure_model_client() -> str:
    """Backup route for docs/RIESGOS.md R8: if the OpenAI credit runs out
    mid-build, setting OPENROUTER_API_KEY switches the same call format over to
    OpenRouter with no refactor. OpenAI wins when both are present.

    Returns the provider actually selected, so the choice is visible rather
    than silent.
    """
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"

    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    if not openrouter_key:
        return "openai"

    from agents import set_default_openai_client
    from openai import AsyncOpenAI

    set_default_openai_client(AsyncOpenAI(api_key=openrouter_key, base_url=OPENROUTER_BASE_URL))
    return "openrouter"


def _run_real_agent(ctx: TurnContext, session: SessionState, message: str) -> str:
    """Real OpenAI Agents SDK loop. Imported lazily so the stub path never
    requires the package to be installed.
    """
    from agents import Agent, Runner, function_tool

    provider = configure_model_client()
    ctx.record("model", f"provider={provider}")

    read_page_tool, fill_field_tool, verify_entity_tool = build_agent_tools(ctx, session)

    # The names the model sees are the ones the frozen contract defines
    # (docs/API_CONTRACTS.md, "Herramientas"), not the Python identifiers.
    agent = Agent(
        name="ventana",
        # ponytail: the SDK default is a reasoning model that takes ~11s per turn,
        # past the contract's 8s timeout. A fast model does the job in ~3s.
        model=os.environ.get("VENTANA_MODEL", DEFAULT_MODEL),
        instructions=build_instructions(ctx.locale),
        tools=[
            function_tool(read_page_tool, name_override="read_page"),
            function_tool(fill_field_tool, name_override="fill_field"),
            function_tool(verify_entity_tool, name_override="verify_entity"),
        ],
    )

    result = Runner.run_sync(agent, build_turn_input(ctx, message))
    return str(result.final_output or "")


def run_turn(request: TurnRequest) -> TurnResponse:
    if request.page is None:
        return error_response(
            request.session_id, request.locale, "missing_page", "page snapshot missing in request"
        )

    ctx = TurnContext(page=request.page, locale=request.locale)
    session = get_session(request.session_id)

    if request.action_results is not None:
        exhausted_labels = _process_action_results(ctx, session, request.action_results)
        reply = _reply_for(request.locale, ctx, session, exhausted_labels, DONE_REPLIES[request.locale])
        return TurnResponse(
            session_id=request.session_id,
            status=_status_for(ctx, session),
            reply=reply,
            actions=ctx.actions,
            trace=ctx.trace,
        )

    if _backend_mode() == "stub":
        _run_stub(ctx, session, request.message)
        model_reply = None
    else:
        try:
            model_reply = _run_real_agent(ctx, session, request.message or "")
        except Exception as exc:  # degrade gracefully — AGENTS.md rule 5
            return error_response(
                request.session_id,
                request.locale,
                "model_error",
                f"model_error: {type(exc).__name__}",
            )

    reply = model_reply or _reply_for(
        request.locale, ctx, session, [], NOTHING_FOUND_REPLIES[request.locale]
    )

    return TurnResponse(
        session_id=request.session_id,
        status=_status_for(ctx, session),
        reply=reply,
        actions=ctx.actions,
        trace=ctx.trace,
    )
