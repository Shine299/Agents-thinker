// Content script: indexes the DOM into a compact, actionable element list and
// (in later sprints) executes approved actions on it. Reasoning never happens
// here — see docs/ARCHITECTURE.md, "dependency rule".

const MAX_ELEMENTS = 150;
const MAX_OPTIONS = 20;
const MAX_BYTES = 6 * 1024;
const INDEXABLE_SELECTOR = "input, select, textarea, button, a[href]";

function textOf(node) {
  return node ? node.textContent.replace(/\s+/g, " ").trim() : "";
}

// Fallback chain per DOMAIN.md: <label for> -> aria-label -> placeholder ->
// previous <td> text -> previous sibling text -> "".
function labelFor(el) {
  if (el.id) {
    const labels = el.ownerDocument.querySelectorAll("label[for]");
    for (const label of labels) {
      if (label.htmlFor === el.id) {
        const text = textOf(label);
        if (text) return text;
        break;
      }
    }
  }

  const ariaLabel = el.getAttribute("aria-label");
  if (ariaLabel && ariaLabel.trim()) return ariaLabel.trim();

  const placeholder = el.getAttribute("placeholder");
  if (placeholder && placeholder.trim()) return placeholder.trim();

  const cell = el.closest("td");
  if (cell) {
    let prev = cell.previousElementSibling;
    while (prev) {
      const text = textOf(prev);
      if (text) return text;
      prev = prev.previousElementSibling;
    }
  }

  let sibling = el.previousSibling;
  while (sibling) {
    const text = textOf(sibling);
    if (text) return text;
    sibling = sibling.previousSibling;
  }

  return "";
}

function isPasswordField(el) {
  return el.tagName === "INPUT" && (el.getAttribute("type") || "").toLowerCase() === "password";
}

function optionsFor(el) {
  if (el.tagName !== "SELECT") return null;
  return Array.from(el.options)
    .slice(0, MAX_OPTIONS)
    .map((opt) => ({ value: opt.value, text: opt.textContent.trim() }));
}

function elementToEntry(el, ref) {
  return {
    ref,
    tag: el.tagName.toLowerCase(),
    type: el.getAttribute("type") || null,
    label: labelFor(el),
    value: "value" in el ? el.value : null,
    options: optionsFor(el),
    required: el.hasAttribute("required"),
  };
}

function serializedSize(elements) {
  return new TextEncoder().encode(JSON.stringify(elements)).length;
}

function indexPage(doc = document) {
  const candidates = Array.from(doc.querySelectorAll(INDEXABLE_SELECTOR)).filter(
    (el) => !isPasswordField(el)
  );

  const tagged = candidates.slice(0, MAX_ELEMENTS).map((el, i) => {
    const ref = `e${i}`;
    // Marks the exact node a ref points to, so a later executeActions() looks
    // it up directly instead of recomputing a position — a node earlier in
    // the DOM disappearing must never make a ref silently resolve to the
    // wrong element.
    el.setAttribute("data-ventana-ref", ref);
    return { el, ref };
  });

  let elements = tagged.map(({ el, ref }) => elementToEntry(el, ref));

  while (elements.length > 0 && serializedSize(elements) > MAX_BYTES) {
    elements = elements.slice(0, elements.length - 1);
  }

  return {
    url: doc.location ? doc.location.href : "",
    title: doc.title || "",
    elements,
  };
}

const REF_NOT_FOUND = "ref_not_found";

// Executes only approved fill_field actions. A plain `el.value = x` does not
// trigger the portal's own validators — real `input`/`change` events with
// bubbles:true do (docs/RIESGOS.md R4). Never throws: an unresolvable ref
// comes back as an ok:false result, so the caller can decide whether to retry.
function executeActions(actions, doc = document) {
  return actions.map((action) => {
    if (action.tool !== "fill_field") {
      return { action_id: action.action_id, ok: false, value: null, error: "unsupported_tool" };
    }

    const { ref, value } = action.args;
    const el = findByRef(ref, doc);
    if (!el) {
      return { action_id: action.action_id, ok: false, value: null, error: REF_NOT_FOUND };
    }

    el.value = value;
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));

    return { action_id: action.action_id, ok: true, value, error: null };
  });
}

// Looks up the exact node indexPage() tagged with this ref. Returns null —
// never guesses at a different element — if that node is gone or was never
// tagged, which is exactly the retry trigger (ref_not_found).
function findByRef(ref, doc) {
  return doc.querySelector(`[data-ventana-ref="${ref}"]`);
}

if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.onMessage) {
  chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (message.type === "PING") {
      sendResponse({ ok: true });
      return true;
    }
    if (message.type === "INDEX_PAGE") {
      sendResponse(indexPage());
      return true;
    }
    if (message.type === "EXECUTE_ACTIONS") {
      sendResponse({ action_results: executeActions(message.actions) });
      return true;
    }
    return false;
  });
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    labelFor,
    indexPage,
    executeActions,
    isPasswordField,
    MAX_ELEMENTS,
    MAX_BYTES,
    MAX_OPTIONS,
  };
}
