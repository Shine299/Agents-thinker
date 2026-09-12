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

- [ ] `docs/API_CONTRACTS.md` está congelado y ambos frentes (A, B) trabajan contra él, no contra acuerdos verbales
- [ ] El indexado nunca incluye `input[type="password"]`
- [ ] El repo público existe con README esqueleto **en inglés** (frente D)
- [ ] `en.json` y `es.json` existen y tienen las mismas claves
- [ ] Todo identificador, comentario y mensaje de commit está en inglés (`docs/I18N_POLICY.md`)
- [ ] `locale` es obligatorio en el contrato y el backend no lo adivina del `message`

--- Bitácora del ciclo (llenar en vivo, con hora) ---
Rojo certificado por Supervisor TDD:   [ ] Sí [ ] No — hora: — motivo:
Verde certificado por Supervisor TDD:  [ ] Sí [ ] No — hora: — motivo:
Dominio puro verificado:               [ ] Sí [ ] No
Contrato con el entorno respetado:     [ ] Sí [ ] No
Corrió con evento/dato real del entorno: [ ] Sí [ ] No
Veredicto final: APROBADO / RECHAZADO
