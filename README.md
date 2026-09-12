# Ventana

**The agent that works inside the tab you already have open.**

Built for *Agents, Everywhere* — AI Tinkerers Lima (global competition), September 12, 2026.

Available in **English and Spanish** — switch languages from the panel header at any time.

---

## The problem

Every AI automation tool assumes the target system has an API. The systems where administrative work actually happens in Latin America don't have one, and never will: government filing desks, university intranets, public service portals, fifteen-year-old ERPs. They are alive, they are mandatory, and they are completely opaque to any agent.

## The thesis

**When there is no API, the browser is the API.**

The agent doesn't use the browser as a conversation channel — it uses it as its only point of access to a system that is otherwise closed to it. What it gets there isn't more context, it's the *only* context possible: the user's already-authenticated session, the current state of the form, the table on screen right now.

This would not work in a chat. The agent needs to be inside the user's session, on the page they are looking at right now.

## What it does

A browser extension with a side panel where an agent lives, sees the active page, and acts on it — **with human approval on every action that changes anything**.

| Flow | Status | What it does |
| --- | --- | --- |
| 1 · Assisted form filling | MVP | Extracts structured data from a pasted email or PDF, maps it to the real fields of the form on screen, and proposes the filling field by field with its reasoning |
| 2 · Table reading | Out of scope for the event | Extracts a case tray from the DOM and answers natural language questions about it |
| 3 · Pre-submission review | Out of scope for the event | Detects empty fields, invalid formats, and inconsistencies before the system rejects them |

**Non-negotiable design principle: the agent never submits.** It can read, it can propose, it can write fields after explicit approval — but the submit button is pressed by the person. The submit tool isn't disabled: it isn't implemented.

## Architecture

```
Browser (legacy portal tab)
  ├─ Content script    → indexes the DOM, assigns refs, executes actions
  ├─ Service worker    → bridge
  └─ Side panel        → input, action plan, approvals, log, ES/EN switch
         │ HTTP
Backend (localhost:8000)
  └─ Agent loop (OpenAI Agents SDK)
     tools: read_page · fill_field · extract_table · verify_entity
         │
       Exa (verify_entity)
```

**The technical core:** we don't send the HTML to the model. A legacy portal page carries between 200 KB and 2 MB of 2009-era markup. What we send is a **compact index of actionable elements** (max 150, ≤6 KB of JSON): each one with a stable `ref`, its `label` resolved through a fallback chain, its value and its options. The model reasons over `ref` + `label`, never over brittle CSS selectors.

**Failure handling:** on `ref_not_found`, the agent re-runs `read_page` once and retries with the fresh index. If it fails again, it stops and reports in plain language. One retry per action, never in a loop, never failing silently. The retry is visible in the panel log.

**Privacy:** indexing excludes every `input[type="password"]`. No credential ever leaves the tab.

Full detail in [`ARCHITECTURE.md`](ARCHITECTURE.md) and [`docs/API_CONTRACTS.md`](docs/API_CONTRACTS.md).

## Bilingual by design

The portals are in Spanish. The people using them work in Spanish. The evaluators are global. So the product ships in both languages:

- Interface strings live in `extension/i18n/en.json` and `es.json` — never hardcoded in the source.
- The active `locale` travels in every `/agent/turn` request, so the agent's `reply` and each `reason` come back in the user's language.
- Switching language keeps the session and its history intact.
- Error codes (`ref_not_found`, `page_stale`) stay technical and untranslated; only their presentation is localized.

Policy and key conventions: [`docs/I18N_POLICY.md`](docs/I18N_POLICY.md).

## Running it

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000

# Demo portal
cd portal-demo && python -m http.server 5500

# Extension
# chrome://extensions → Developer mode → Load unpacked → extension/ folder
```

The backend runs locally. There is no deployment: in a one-day event, a public URL adds nothing to the score, and the 30–40 minutes saved do. Google Cloud Run is documented as the future deployment plan — its permanent free tier covers this project comfortably.

## What was built during the hackathon

| Component | Type |
| --- | --- |
| DOM indexing, `labelFor` fallback chain, action execution | **Built during the event** |
| The four tools, the system prompt, approval and retry logic | **Built during the event** |
| The `/agent/turn` contract, the full side panel, the i18n layer, the cloned portal and the demo case | **Built during the event** |
| OpenAI Agents SDK (agent loop and tool calling) | Permitted library, pre-existing |
| MV3 manifest boilerplate | Standard Chrome pattern, pre-existing |
| Exa API | Sponsor service, pre-existing |

## Known limitations

*(Filled in at 14:30, at code freeze. Any bug found after that hour is documented here instead of being fixed — a project delivered at 70% scores; one at 95% never submitted scores zero.)*

- [ ] …
- [ ] …

## Methodology

Built applying SDD + TDD + Scrum compressed into 4 sprints inside a real 4h15 window, with a **TDD Supervisor** role holding veto power over closing any task. The full documentation set lives in this repo (internal working docs are in Spanish; the team built in Spanish, the product and the code are in English):

| File | Contents |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Operating rules for both roles |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Layers, data flow, dependency rule |
| [`TECH_STACK.md`](TECH_STACK.md) | Allowed and banned technologies, justified |
| [`DOMAIN.md`](DOMAIN.md) | Glossary and naming conventions |
| [`MEMORY.md`](MEMORY.md) | Retrospective, eligibility log, out of scope |
| [`.sprints/BACKLOG.md`](.sprints/BACKLOG.md) | The 4 sprints and their decision points |
| [`docs/I18N_POLICY.md`](docs/I18N_POLICY.md) | Language policy, binding under SDD |
| [`docs/`](docs/) | Challenge understanding, strategy, API contract, risks, video script, sponsor credits |
