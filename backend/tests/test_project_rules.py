"""Guardrails for the project rules the Supervisor TDD checks by hand at every
Verde (AGENTS.md rule 15, docs/I18N_POLICY.md section 6). Automating them means
they cannot be forgotten under time pressure.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXTENSION = REPO_ROOT / "extension"


def test_agent_backend_defaults_to_the_real_model_not_the_stub():
    """A forgotten env var must not silently serve mocked answers in the demo.
    Missing configuration should fail loudly on a real call instead.
    """
    import agent

    saved = os.environ.pop("VENTANA_AGENT_BACKEND", None)
    try:
        assert agent._backend_mode() != "stub"
    finally:
        if saved is not None:
            os.environ["VENTANA_AGENT_BACKEND"] = saved


def test_panel_never_assigns_a_hardcoded_visible_string():
    """Every user-visible string must come from t(). Catches
    `el.textContent = "Campos detectados"` (docs/I18N_POLICY.md section 2).
    """
    source = (EXTENSION / "panel.js").read_text()

    offenders = re.findall(r"\.(?:textContent|placeholder|innerText)\s*=\s*[\"'][^\"']+[\"']", source)

    assert offenders == [], f"Hardcoded visible strings in panel.js: {offenders}"


def test_no_submit_tool_exists_anywhere_in_the_backend():
    """The submit tool is not disabled — it must not exist at all
    (docs/API_CONTRACTS.md, non-negotiable rules).
    """
    backend = Path(__file__).resolve().parent.parent
    sources = list(backend.glob("*.py"))

    # Looks for an actual definition or registration, not prose: the system
    # prompt legitimately contains the word while forbidding the behaviour.
    patterns = [
        r"def\s+\w*submit\w*\s*\(",
        r"tool\s*=\s*[\"']submit",
        r"function_tool\(\s*\w*submit",
    ]

    offenders = [
        path.name
        for path in sources
        if any(re.search(p, path.read_text()) for p in patterns)
    ]

    assert offenders == [], f"Something resembling a submit tool appears in: {offenders}"


def test_indexing_excludes_password_fields_by_construction():
    """The content script must filter password inputs out of the index
    (docs/API_CONTRACTS.md, non-negotiable rules).
    """
    source = (EXTENSION / "content.js").read_text()

    assert "isPasswordField" in source
    assert 'password' in source


def test_no_dead_i18n_keys():
    """A key defined in the dictionaries but never referenced anywhere is
    exactly the kind of leftover an audit under time pressure misses — an
    earlier pass in this project left three such keys behind. en/es parity
    is covered separately by test_i18n_parity.py; this catches the other
    failure mode: a key both files agree on, that nothing ever reads.
    """
    import json

    en = json.loads((EXTENSION / "i18n" / "en.json").read_text())
    js_sources = "\n".join(
        (EXTENSION / name).read_text() for name in ("panel.js", "content.js")
    )

    dead = [key for key in en if key not in js_sources]

    assert dead == [], f"i18n keys defined but never referenced: {dead}"
