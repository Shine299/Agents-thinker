// Runs both browser test benches headlessly under jsdom and prints PASS/FAIL
// counts. One-time setup (from this folder): npm install --no-save jsdom
// Then: node run-benches.mjs   (exit code 1 if any check fails)
import { JSDOM } from "jsdom";
import { readFileSync } from "fs";
import { createServer } from "http";
import { dirname, extname, join } from "path";
import { fileURLToPath } from "url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const PORT = 5599;

// Tiny static server: test-panel.html loads i18n/*.json and panel.js by
// relative URL, and test-index.html loads ../extension/content.js.
const server = createServer((req, res) => {
  try {
    res.setHeader("Content-Type", extname(req.url) === ".json" ? "application/json" : "text/html");
    res.end(readFileSync(join(ROOT, decodeURIComponent(req.url.split("?")[0]))));
  } catch {
    res.statusCode = 404;
    res.end();
  }
}).listen(PORT);

// jsdom has no fetch; the panel bench reads the real dictionaries from here.
const i18n = {
  en: JSON.parse(readFileSync(join(ROOT, "extension/i18n/en.json"), "utf8")),
  es: JSON.parse(readFileSync(join(ROOT, "extension/i18n/es.json"), "utf8")),
};

let failed = 0;
for (const bench of ["portal-demo/test-index.html", "extension/test-panel.html"]) {
  const dom = await JSDOM.fromURL(`http://localhost:${PORT}/${bench}`, {
    runScripts: "dangerously",
    resources: "usable",
    beforeParse(window) { window.__i18nFixtures = i18n; },
  });
  await new Promise((r) => setTimeout(r, 2500)); // benches are async
  const text = dom.window.document.getElementById("results").textContent;
  const pass = (text.match(/PASS/g) || []).length;
  const fail = (text.match(/FAIL/g) || []).length;
  failed += fail;
  console.log(`${bench}: ${pass} PASS / ${fail} FAIL`);
  if (fail) console.log(text);
}
server.close();
process.exit(failed ? 1 : 0);
