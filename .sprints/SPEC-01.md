# SPEC-01: Scaffolding + contrato congelado + mocks (11:15–12:00)

Criterio de rúbrica objetivo: **A** (requisitos y funcionalidad — sin esto no hay proyecto)
Pre-existente o construido hoy: manifest MV3 es patrón estándar de Chrome (pre-existente); indexado, agent loop sobre mock y portal clonado se construyen hoy.

## Escenario 1 — Indexado de página (frente A)

Given: el side panel está abierto sobre una pestaña con el portal clonado cargado
When: el panel envía `INDEX_PAGE` al content script
Then: recibe `{ url, title, elements[] }` con máximo 150 elementos, cada uno con `ref`, `tag`, `label` y `value`

## Escenario 2 — Agent loop contra mock (frente B)

Given: un payload de ejemplo con `page.elements` fijo (mock del contrato congelado)
When: se llama `POST /agent/turn` con ese payload y un `message` de prueba
Then: la respuesta tiene `status: "awaiting_approval"`, al menos una `action` con `reason`, y un `trace` no vacío

## Escenario 3 — Portal clonado sirviendo (frente C)

Given: un portal real de trámites guardado con `Save page as → Complete`
When: se sirve con `python -m http.server 5500`
Then: el formulario carga en `localhost:5500` conservando su markup original (tablas anidadas, IDs crípticos)

## Escenario 4 — Andamiaje i18n desde el primer commit (frentes A y B)

Given: el panel se abre por primera vez y `chrome.i18n.getUILanguage()` devuelve `es-PE`
When: se renderizan los textos de la cabecera y del input
Then: todos salen de `t()` leyendo `extension/i18n/es.json` — cero strings hardcodeados en el código

Given: una petición a `/agent/turn` con `locale: "en"`
When: el agente responde
Then: `reply` y cada `reason` están redactados en inglés, sin mezclar idiomas

## Criterios de aceptación (DoD)

- [x] `docs/API_CONTRACTS.md` está congelado y ambos frentes (A, B) trabajan contra él, no contra acuerdos verbales
- [x] El indexado nunca incluye `input[type="password"]` — verificado en `portal-demo/test-index.html` y sobre `mesa-partes.html` real (12 elementos indexados, 0 passwords)
- [ ] El repo público existe con README esqueleto **en inglés** (frente D) — **NO CUMPLIDO.** El README está escrito en inglés y sus enlaces resuelven, pero **no existe repo público**: falta ejecutar `gh repo create` (guía M3). Única casilla abierta del sprint
- [x] `en.json` y `es.json` existen y tienen las mismas claves — certificado por `backend/tests/test_i18n_parity.py`
- [x] Todo identificador, comentario y mensaje de commit está en inglés (`docs/I18N_POLICY.md`)
- [x] `locale` es obligatorio en el contrato y el backend no lo adivina del `message` — certificado por `test_agent_turn_requires_locale` (422 sin `locale`)

--- Bitácora del ciclo (llenar en vivo, con hora) ---

**Pasada 1 (RECHAZADA en auditoría).**
Verde declarado: 13:23 — 6/6 pytest + 10/10 banco de pruebas.
Rojo: **nunca existió.** La bitácora original afirmaba un ciclo Rojo→Verde que no ocurrió: el código
(`contracts.py`, `tools.py`, `agent.py`, `main.py`) se escribió **antes** que los tests. Violación de la
regla 2 de `AGENTS.md`. Auditoría posterior encontró además 4 defectos funcionales y 2 tests vacuos.
Veredicto pasada 1: **RECHAZADO** — ver `MEMORY.md` § "Auditoría de Sprint-01".

**Pasada 2 (TDD real).**
Rojo certificado:  [x] Sí — hora: 14:02 — motivo: `pytest tests/test_agent_real_path.py tests/test_error_handling.py`
  → `ImportError: cannot import name 'build_agent_tools'` + 4 failed. Evidencia capturada antes de tocar código.
Verde certificado: [x] Sí — hora: 14:31 — motivo: `pytest tests/ -q` → **26 passed** (contrato x5, camino real del
  agente x11, manejo de errores x4, reglas de proyecto x4, paridad i18n x1, respaldo OpenRouter x2);
  banco de pruebas del navegador → **13/13 PASS**, con los topes de 150 elementos y 6 KB ejercitados de verdad.
Dominio puro verificado:               [x] Sí — `backend/tools.py` no importa FastAPI ni nada de `extension/`
Contrato con el entorno respetado:     [x] Sí — `contracts.py` 1:1 con `docs/API_CONTRACTS.md`; `locale` obligatorio (422);
  todo fallo devuelve `TurnResponse` con `status: "error"`, nunca un envelope HTTP; nombres de herramienta = los del contrato
Corrió con evento/dato real del entorno: [x] Sí — `indexPage()` sobre `mesa-partes.html` real (12 elementos, 0 passwords);
  `/agent/turn` en modo real degradando con mensaje legible en `es` y `en` sin clave
Veredicto final: **APROBADO con 1 salvedad** — la casilla del repo público queda abierta (acción manual M3,
no ejecutable por el agente sin confirmación del humano).
