# SPEC-02: Llenado real, aprobación, Exa (12:30–13:30)

Criterio de rúbrica objetivo: **C** (ejecución técnica) y **D** (control del usuario)
Pre-existente o construido hoy: Exa API es servicio de sponsor (pre-existente); la herramienta `verify_entity`, el flujo de aprobación y el reintento se escriben hoy.

Requisito previo: Punto de Decisión 1 (12:30) cerrado en Verde o Ámbar por el Supervisor TDD. Si fue Rojo, este SPEC no se abre hasta activar el plan B (Slack) y re-certificar.

## Escenario 1 — Llenado dispara validadores reales

Given: un campo de texto vacío en el formulario clonado, con `ref = e12`
When: el agente ejecuta `fill_field` con `{ ref: "e12", value: "Juan Pérez Quispe" }`
Then: el campo muestra el valor Y el portal lo reconoce como válido (los eventos `input`/`change` con `bubbles: true` se dispararon)

## Escenario 2 — Ninguna acción sin aprobación

Given: el agente propuso 8 acciones de `fill_field`
When: el usuario aprueba solo 5 de ellas
Then: únicamente esas 5 se ejecutan sobre el DOM; las otras 3 quedan pendientes

## Escenario 3 — Reintento único ante `ref_not_found`

Given: una acción de `fill_field` referencia un `ref` que ya no existe en el DOM
When: se ejecuta la acción
Then: el agente re-ejecuta `read_page` una vez, reintenta con el índice nuevo, y si vuelve a fallar se detiene y lo reporta en el panel — visible en el `trace`, nunca en bucle

## Escenario 4 — Verificación externa vía Exa

Given: el correo de demo menciona una empresa que debe validarse
When: el agente detecta ese dato como verificable
Then: llama `verify_entity` y el resultado de Exa aparece en el `trace` antes de proponer el campo correspondiente

## Escenario 5 — Cambio de idioma en caliente

Given: una sesión activa en español con 8 acciones ya propuestas
When: el usuario pulsa el selector EN en la cabecera
Then: los textos de interfaz cambian a inglés, la elección persiste en `chrome.storage.local`, el historial de la sesión NO se pierde, y las respuestas siguientes del agente llegan en inglés

## Escenario 6 — Errores traducidos, códigos técnicos ocultos

Given: una acción falla con `ref_not_found`
When: el panel muestra el fallo
Then: el usuario ve el texto de `error.refNotFound` en su idioma activo; el código crudo `ref_not_found` aparece solo en el `trace`, nunca en el mensaje al usuario

## Criterios de aceptación (DoD)

- [x] El caso de demo (correo ficticio, 8-10 campos, 1 dato verificable por Exa, 1 dato que requiere transformación) está listo **y operativo**: `verify_entity` se llama de verdad cuando el mensaje menciona una empresa/RUC, verificado por HTTP real (ver bitácora)
- [x] Ninguna acción con `needs_approval: true` se ejecuta sin clic del usuario — `fill_field` siempre fija `needs_approval: true`; el panel solo llama `EXECUTE_ACTIONS` desde `approveAction()`
- [x] Los `label` del formulario y los `ref` se citan textualmente dentro de `reason`, sin traducirse
- [x] Ningún string visible al usuario quedó hardcodeado en `extension/` ni en `backend/` — certificado por `test_panel_never_assigns_a_hardcoded_visible_string` y `test_no_dead_i18n_keys` (nuevo: ninguna clave sin usar tampoco)

--- Bitácora del ciclo (llenar en vivo, con hora) ---

**Pasada 1 (RECHAZADA en auditoría, 14:20).** Verde autodeclarado tras implementar `fill_field` real, aprobación, reintento, Exa (tool construido) y selector ES/EN.
Auditoría estricta contra este mismo SPEC encontró:
- `verify_entity` construido y testeado en aislamiento, pero **nunca invocado** por el agente (stub ni real) — Escenario 4 incumplido de facto.
- Bug de estado real, reproducido con datos: aprobar 1 de 3 campos hacía que el backend respondiera `status: "done"` / *"listo, completado"* mientras 2 campos seguían vacíos — violación directa del Escenario 2.
- `error.refNotFound` definida pero sin un solo uso real en el panel.
- Cero tests automatizados de `panel.js` (0 de 58 verificaciones totales cubrían la UI).
Veredicto pasada 1: **RECHAZADO.**

**Pasada 2 (TDD real, 14:25–15:10).**
Rojo certificado: [x] Sí — hora: 14:31 — `pytest tests/test_partial_approval.py tests/test_verify_entity_wiring.py tests/test_agent_real_path.py` → 8 failed (ValueError por desempaquetado de 2 valores donde ya hacían falta 3, y el "done" prematuro reproducido en test). Banco de pruebas de `panel.js` (`extension/test-panel.html`, nuevo): no existía.
Verde certificado: [x] Sí — hora: 15:10 — `pytest tests/ -v` → **44/44**; banco de `content.js` → **19/19**; banco nuevo de `panel.js` (vía jsdom, DOM real de `panel.html` + mocks de `chrome.*`/`fetch`) → **14/14**. Total: **77 verificaciones automatizadas**.
Corrección de la bitácora: se documenta el Rojo real de la pasada 2, no un Rojo retroactivo inventado para la pasada 1.
Dominio puro verificado: [x] Sí — `session_store.py`/`tools.py` sin imports de FastAPI ni de la extensión.
Contrato con el entorno respetado: [x] Sí — `error: "discarded"` se añadió como valor libre de un campo `Optional[str]` ya existente en el contrato, sin tocar su forma; ninguna herramienta de envío existe.
Corrió con evento/dato real del entorno: [x] Sí — HTTP real contra `localhost:8000` con el caso de demo completo (Juan Pérez Quispe / GRUPO ANDINO SAC / RUC 20456789123): `verify_entity` aparece en el paso 2 del `trace`, antes de los 3 `fill_field`. `executeActions()` verificado en Chrome real sobre `mesa-partes.html` (ver `MEMORY.md`), disparando el validador `onchange` nativo del portal.
Veredicto final: **APROBADO**, con una tarea pendiente explícita fuera de este SPEC: verificación real con clave de Exa/OpenAI (el equipo aún no las canjea; el modo `stub` cubre el contrato mientras tanto).
