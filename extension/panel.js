// Side panel UI: connection status, indexing, the real turn loop against
// /agent/turn, per-row approval, and the ES/EN switch. No reasoning lives
// here — this only renders what the backend proposes and executes only what
// the user approved (docs/ARCHITECTURE.md, "dependency rule").

const BACKEND_URL = "http://localhost:8000";

// One id for the lifetime of this panel instance. Switching locale must not
// reset it — that is what keeps the session's history intact
// (docs/I18N_POLICY.md section 5.4).
const sessionId = crypto.randomUUID();

let pendingActions = [];
let traceLog = [];

function renderStrings() {
  document.getElementById("panelTitle").textContent = t("panel.title");
  document.getElementById("indexBtn").textContent = t("page.indexNow");
  document.getElementById("messageInput").placeholder = t("input.placeholder");
  document.getElementById("submitBtn").textContent = t("input.submit");
  document.getElementById("actionsTitle").textContent = t("action.planTitle");
  document.getElementById("traceTitle").textContent = t("trace.title");
  renderActions();
  renderTrace();

  const active = getLocale();
  document.getElementById("localeEsBtn").classList.toggle("active", active === "es");
  document.getElementById("localeEnBtn").classList.toggle("active", active === "en");
}

function setStatus(connected) {
  const el = document.getElementById("status");
  el.textContent = connected ? t("panel.connected") : t("panel.disconnected");
  el.className = connected ? "connected" : "disconnected";
}

async function checkHealth() {
  try {
    const res = await fetch(`${BACKEND_URL}/health`, { method: "GET" });
    setStatus(res.ok);
    return res.ok;
  } catch (_err) {
    setStatus(false);
    return false;
  }
}

function getActiveTabId() {
  return new Promise((resolve) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      resolve(tabs[0] && tabs[0].id);
    });
  });
}

async function sendToContentScript(message) {
  const tabId = await getActiveTabId();
  if (!tabId) {
    throw new Error("no_active_tab");
  }
  return new Promise((resolve, reject) => {
    chrome.tabs.sendMessage(tabId, message, (response) => {
      if (chrome.runtime.lastError || !response) {
        reject(new Error("content_script_unreachable"));
        return;
      }
      resolve(response);
    });
  });
}

async function readCurrentPage() {
  return sendToContentScript({ type: "INDEX_PAGE" });
}

async function postTurn(body) {
  const response = await fetch(`${BACKEND_URL}/agent/turn`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, locale: getLocale(), ...body }),
  });
  return response.json();
}

function renderReply(text, isError) {
  const el = document.getElementById("replyArea");
  el.textContent = text || "";
  el.className = isError ? "error" : "ok";
}

function renderLoading() {
  renderReply(t("state.loading"), false);
}

function renderActions() {
  const container = document.getElementById("actions");
  const emptyLabel = document.getElementById("actionsEmpty");
  container.innerHTML = "";

  emptyLabel.textContent = pendingActions.length === 0 ? t("state.empty") : "";

  for (const action of pendingActions) {
    const row = document.createElement("div");
    row.className = "action-row";
    row.dataset.actionId = action.action_id;

    const reason = document.createElement("div");
    reason.className = "reason";
    reason.textContent = action.reason;
    row.appendChild(reason);

    const buttons = document.createElement("div");
    buttons.className = "row-buttons";

    const approveBtn = document.createElement("button");
    approveBtn.textContent = t("action.approve");
    approveBtn.addEventListener("click", () => approveAction(action));

    const discardBtn = document.createElement("button");
    discardBtn.textContent = t("action.discard");
    discardBtn.addEventListener("click", () => discardAction(action));

    buttons.appendChild(approveBtn);
    buttons.appendChild(discardBtn);
    row.appendChild(buttons);

    container.appendChild(row);
  }
}

// Gives immediate feedback for the round trip to the backend: the row stays
// visible (not yet removed — that only happens once the backend confirms
// what to do with it) but shows it is no longer waiting on the user.
function markRowApproved(actionId) {
  const row = document.querySelector(`.action-row[data-action-id="${actionId}"]`);
  if (!row) return;
  row.classList.add("approved");
  const buttons = row.querySelector(".row-buttons");
  if (buttons) buttons.textContent = t("action.approved");
}

function renderTrace() {
  const container = document.getElementById("trace");
  container.innerHTML = "";
  for (const step of traceLog) {
    const line = document.createElement("div");
    line.className = "trace-step";
    const toolLabel = step.tool === "retry" ? t("trace.retry") : step.tool;
    line.textContent = `${step.step}. ${toolLabel} — ${step.outcome}`;
    container.appendChild(line);
  }
}

function appendTrace(steps) {
  traceLog = traceLog.concat(steps || []);
  renderTrace();
}

function mergeActions(newActions) {
  pendingActions = pendingActions.concat(newActions || []);
  renderActions();
}

function removeAction(actionId) {
  pendingActions = pendingActions.filter((a) => a.action_id !== actionId);
  renderActions();
}

async function handleSubmit() {
  const message = document.getElementById("messageInput").value;
  if (!message.trim()) return;

  renderLoading();

  let page;
  try {
    page = await readCurrentPage();
  } catch (_err) {
    renderReply(t("error.pageUnreachable"), true);
    return;
  }

  let response;
  try {
    response = await postTurn({ message, page, action_results: null });
  } catch (_err) {
    renderReply(t("error.backendUnreachable"), true);
    return;
  }

  renderReply(response.reply, response.status === "error");
  mergeActions(response.actions);
  appendTrace(response.trace);
}

async function approveAction(action) {
  markRowApproved(action.action_id);
  renderLoading();

  let execResult;
  try {
    execResult = await sendToContentScript({ type: "EXECUTE_ACTIONS", actions: [action] });
  } catch (_err) {
    renderReply(t("error.pageUnreachable"), true);
    return;
  }

  let page;
  try {
    page = await readCurrentPage();
  } catch (_err) {
    renderReply(t("error.pageUnreachable"), true);
    return;
  }

  let response;
  try {
    response = await postTurn({
      message: null,
      page,
      action_results: execResult.action_results,
    });
  } catch (_err) {
    renderReply(t("error.backendUnreachable"), true);
    return;
  }

  removeAction(action.action_id);
  renderReply(response.reply, response.status === "error");
  mergeActions(response.actions);
  appendTrace(response.trace);
}

async function discardAction(action) {
  // Discarding never touches the DOM — no EXECUTE_ACTIONS is sent. The
  // backend still needs to hear about it, though: without this it would
  // keep treating the discarded field as unresolved forever (never "done").
  removeAction(action.action_id);
  renderLoading();

  let page;
  try {
    page = await readCurrentPage();
  } catch (_err) {
    renderReply(t("error.pageUnreachable"), true);
    return;
  }

  let response;
  try {
    response = await postTurn({
      message: null,
      page,
      action_results: [{ action_id: action.action_id, ok: false, value: null, error: "discarded" }],
    });
  } catch (_err) {
    renderReply(t("error.backendUnreachable"), true);
    return;
  }

  renderReply(response.reply, response.status === "error");
  mergeActions(response.actions);
  appendTrace(response.trace);
}

async function indexActivePage() {
  try {
    const page = await readCurrentPage();
    document.getElementById("indexInfo").textContent =
      t("page.elementsDetected", { count: page.elements.length }) + " — " + t("page.noPasswords");
  } catch (_err) {
    document.getElementById("indexInfo").textContent = t("error.pageUnreachable");
  }
}

async function handleLocaleChange(locale) {
  // Re-renders interface strings only. pendingActions and traceLog are left
  // untouched: switching language never resets the session or drops its
  // history (docs/I18N_POLICY.md section 5.4).
  await setLocale(locale);
  renderStrings();
}

async function init() {
  await initLocale();
  renderStrings();
  await checkHealth();

  document.getElementById("indexBtn").addEventListener("click", indexActivePage);
  document.getElementById("submitBtn").addEventListener("click", handleSubmit);
  document.getElementById("localeEsBtn").addEventListener("click", () => handleLocaleChange("es"));
  document.getElementById("localeEnBtn").addEventListener("click", () => handleLocaleChange("en"));
}

// Minimal introspection seam for automated tests (extension/test-panel.html).
// No production behavior depends on this; it only exposes state that would
// otherwise be invisible to a test driving the page from outside.
if (typeof window !== "undefined") {
  window.__ventanaPanel = {
    getSessionId: () => sessionId,
    getPendingActions: () => pendingActions,
    getTraceLog: () => traceLog,
  };
}

init();
