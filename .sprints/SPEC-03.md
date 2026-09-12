# SPEC-03: Integración real end-to-end + manejo de errores (13:30–14:30)

Criterio de rúbrica objetivo: **A** (funcionalidad end-to-end real) y **C** (manejo de fallos)
Pre-existente o construido hoy: todo se construye/integra hoy — esta es la fase donde desaparecen los mocks del Sprint-01.

## Escenario 1 — Fin de los mocks

Given: la extensión (frente A) y el backend (frente B) ya certificaron Verde por separado contra el contrato
When: el panel llama al backend real (no al mock) con un evento real del portal clonado
Then: la respuesta real se pinta en el panel, con el mismo formato que el mock — sin cambios de contrato de último minuto

## Escenario 2 — Mensajes de error legibles

Given: ocurre un `model_error` o un `ref_not_found` sin recuperación posible
When: el backend responde `status: "error"`
Then: el panel muestra un mensaje en español claro, no un stack trace ni un código crudo

## Escenario 3 — Prueba end-to-end en bucle

Given: el flujo 1 completo (pegar correo → plan → aprobar → llenado → confirmación)
When: se ejecuta 3 veces seguidas sin reiniciar el navegador
Then: las 3 corridas completan sin intervención manual fuera del panel (frente C prueba esto sin parar durante todo el sprint)

## Escenario 4 — Paridad de diccionarios (test automatizado)

Given: los archivos `en.json` y `es.json`
When: corre la suite de tests
Then: el test falla si existe una clave en un archivo y no en el otro. Es un fallo de test, no una advertencia

## Escenario 5 — End-to-end bilingüe

Given: el Flujo 1 completo
When: se ejecuta una corrida en `locale: "es"` y otra en `locale: "en"`
Then: ambas completan sin intervención manual, y ninguna respuesta mezcla idiomas

## Criterios de aceptación (DoD)

- [x] Cero llamadas a datos mockeados quedan en el código de producción — `grep -in "mock" extension/panel.js extension/content.js` → 0 resultados
- [ ] El primer corte del video (frente D) muestra al menos una corrida real, aunque no sea la final — pendiente de grabación (bloque E)

--- Bitácora del ciclo (llenar en vivo, con hora) ---
Rojo certificado por Supervisor TDD: [x] Sí — hora: 2026-09-12 (verificación con claves reales) — motivo: `RateLimitError` (sin crédito), `timeout after 8s`, refs inventados por el modelo, `locale` ignorado — ver `MEMORY.md` "Verificación con claves reales"
Verde certificado por Supervisor TDD: [x] Sí — hora: 2026-09-12 — `pytest tests/ -q` → 46/46; `node extension/run-benches.mjs` → 20+15; E2E por HTTP 6/6 (3× ES/EN) sobre el caso de demo completo con OpenAI + Exa reales
Dominio puro verificado: [x] Sí — `tools.py`/`agent.py` sin imports de FastAPI ni de la extensión
Contrato con el entorno respetado: [x] Sí, con una excepción documentada — timeout 8→20s (`docs/API_CONTRACTS.md`), solo el valor, no la forma
Corrió con evento/dato real del entorno: [x] Sí por HTTP (6/6) — [ ] Pendiente desde el panel en Chrome real (Escenario 3, bloque B de la ejecución de hoy)
Veredicto final: **APROBADO** — Escenarios 1, 2, 4, 5 cerrados con evidencia real; Escenario 3 (bucle desde el panel) y el primer corte de video quedan como única fila abierta, a completar en Chrome antes del Punto de Decisión 2

---

## Auditoría de Punto de Decisión 2 (14:30 — congelamiento absoluto)

| # | Pregunta | Verde/Ámbar/Rojo | Evidencia / Acción si no es Verde |
| --- | --- | --- | --- |
| 1 | ¿El flujo 1 corre end-to-end sobre el portal clonado, con una entrada nueva, ahora mismo? | Verde (por HTTP) | 6/6 corridas reales contra `mesa-partes.html` indexado con `content.js`. Falta la confirmación con clic real en Chrome — anotar aquí el resultado del bloque B |
| 2 | ¿El entorno (navegador + sesión) sigue siendo protagonista o se volvió wrapper por falta de tiempo? | Ámbar hasta la corrida en Chrome | El diseño no cambió (índice del DOM, sesión ya autenticada); falta verificarlo con ojos humanos sobre Chrome real, no solo por HTTP |
| 3 | ¿Las llamadas a Exa/OpenAI son reales o quedó algo simulado? | **Verde** | Confirmado hoy: `provider=openai`, `exa: found — ...` en el `trace` de las 6 corridas reales. `VENTANA_AGENT_BACKEND=stub` queda comentado en `.env.example`, nunca activo por defecto |
| 4 | ¿Un usuario entendería el valor del panel sin explicación extra? | Ámbar | El `reason` de cada propuesta ya lo explica: cita el label exacto y, cuando aplica, la discrepancia de `verify_entity`. Pendiente de juicio humano viendo el panel en vivo |
| 5 | ¿El plan B (OpenRouter si se agota el crédito) está probado o solo documentado? | **Verde** | Probado hoy con clave real: `chat.completions.create` vía OpenRouter respondió "Ok!"; `test_openrouter_is_used_as_the_backup_route...` cubre el cableado |
| 6 | ¿README, guion de video y post social están en progreso real (frente D)? | **Verde** | README con limitaciones y elegibilidad completas hoy; `docs/GUION_VIDEO.md` con la corrida guionizada lista; post social pendiente para Sprint-04 (no es de este sprint) |
| 7 | ¿El README público está íntegramente en inglés, sin español residual? | **Verde** | Revisado íntegro en este cierre; ninguna sección en español |
| 8 | ¿Quedó algún string visible hardcodeado, o alguna clave desalineada entre `en.json` y `es.json`? | **Verde** | `test_i18n_parity.py` (paridad de claves) y `test_no_dead_i18n_keys` (sin claves muertas) — ambos en la suite verde de 46 |

**Regla dura de esta auditoría:** cualquier fila en Rojo a las 14:30 se declara como limitación conocida en el README — no se abre tarea nueva para arreglarla. Las filas 1, 2 y 4 quedan en Ámbar a la espera del resultado real en Chrome (bloque B); pasan a Verde o a limitación conocida según lo que se observe, nunca se dejan sin veredicto.
