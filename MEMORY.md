# MEMORY.md

Retrospectiva continua del proyecto Ventana. Se actualiza en vivo, con hora, por ambos roles (Development Team y Supervisor TDD).

## Resumen de sprints (actualizado 15:10)

| Sprint | Estado | Veredicto | Evidencia |
| --- | --- | --- | --- |
| **Sprint-01** — scaffolding, contrato, mocks | **COMPLETADO** | APROBADO (pasada 2, tras auditoría) | `.sprints/SPEC-01.md` — 6/6 pytest + 10/10 banco de `content.js` en la primera auditoría; corregido a 26 tests / 13 checks en la segunda |
| **Sprint-02** — llenado real, aprobación, reintento, Exa | **CERRADO** | APROBADO (pasada 3, con claves reales) | `.sprints/SPEC-02.md` — 46/46 pytest + 20/20 banco de `content.js` + 15/15 banco de `panel.js` + 6/6 E2E por HTTP con OpenAI y Exa reales |
| **Sprint-03** — integración real, prompt afinado, E2E bilingüe | **En progreso** | 4 de 6 filas Done por HTTP (`.sprints/SPEC-03.md`); falta la corrida desde el panel en Chrome real y el primer corte de video | `.sprints/SPEC-03.md`, `docs/GUION_VIDEO.md` (corrida guionizada añadida), `README.md` (limitaciones + elegibilidad completadas) |
| **Punto de Decisión 1** (12:30) | **Verde** | Extensión cargada y probada en Chrome real | Ver fila de la tabla de abajo |

**Claves de OpenAI y Exa ya activas** (`backend/.env`, 2026-09-12). El flujo corre con modelo real por defecto. Ver [`docs/PENDIENTES.md`](docs/PENDIENTES.md) para operar las claves y el modelo. **Pendiente humano, ahora unificado:** una sola sesión en Chrome real (extensión + backend + portal, los tres ya arriba en `:8000`/`:5500`) cubre a la vez la grabación de pantalla de Sprint-02 y la corrida E2E ×3 de Sprint-03 — ver bloque B del plan de ejecución.

## Estado del sistema (actualizar en cada cierre de tarea)

| Hora | Frente | Componente | Estado | Nota |
| --- | --- | --- | --- | --- |
| 13:23 | — | Reorganización del repo (`docs/`, `.sprints/`, raíz) | Verde | `git mv` desde `files/` a la estructura de `ARCHITECTURE.md`; enlaces de `README.md`/`AGENTS.md` verificados, todos resuelven |
| 13:23 | C | `portal-demo/mesa-partes.html` + `demo-case.txt` + `test-index.html` | Verde | Portal sintético feo a propósito (tablas anidadas, IDs `ctl00_cphMain_*`, sin `<label for>` en la mayoría). 12 elementos indexables, 1 password excluido. Caso de demo: correo de Juan Pérez Quispe / Grupo Andino SAC |
| 13:23 | A | `extension/` (manifest MV3, content.js, background.js, panel.html/js, i18n) | Verde (sin probar en Chrome real — pendiente M2) | `indexPage()`/`labelFor()` verificados vía jsdom: 10/10 checks PASS sobre el banco de pruebas, y corrida real sobre `mesa-partes.html` (12 elementos, 0 passwords, refs únicos) |
| 13:23 | B | `backend/` (`contracts.py`, `tools.py`, `agent.py`, `main.py`) | Verde | `/health` y `/agent/turn` respondiendo real vía `uvicorn`; 6/6 tests pytest en modo `stub`; `locale` obligatorio (422 si falta); respuesta en `es`/`en` verificada |
| 13:23 | D | README / SPEC-01 bitácora / BACKLOG | En progreso | README ya en inglés, enlaces verificados. Falta: `gh repo create` (manual, M3), guion de video, grabación |
| 14:31 | B | Backend tras auditoría (`tools.TurnContext`, `agent.py`, `main.py`) | Verde (pasada 2) | 4 defectos funcionales corregidos con TDD real (Rojo capturado a las 14:02). Suite: 6 → **26 tests** |
| 14:31 | A | `extension/` tras auditoría | Verde | Puente del service worker corregido, clave `error.pageUnreachable` añadida, `t()` ya no falla en silencio. Banco de pruebas: 10 → **13 checks**, con topes ejercitados de verdad |
| 14:00 | — | **PUNTO DE DECISIÓN 1** | **Verde** | Extensión cargada en Chrome real por el humano (guía M2). Sin errores en `chrome://extensions`. Panel abrió sobre `localhost:5500`, mostró "Connected", "Read page" devolvió "12 fields detected... Password fields are never indexed" — coincide exactamente con la verificación por API hecha antes. Plan A confirmado, no se activa el plan B (Slack) |
| 15:10 | B | Backend Sprint-02 tras auditoría (`agent.py`, `tools.py`, `session_store.py` nuevo) | Verde (pasada 2) | 2 defectos graves + 1 gap de cobertura corregidos con TDD real (Rojo capturado a las 14:31). Suite: 35 → **44 tests** |
| 15:10 | A | `extension/panel.js` tras auditoría | Verde | `discardAction` ahora avisa al backend; claves `state.loading`/`action.approved`/`trace.retry` puestas en uso real; 3 claves muertas eliminadas. Banco de pruebas nuevo (`extension/test-panel.html`, vía jsdom + mocks de `chrome.*`/`fetch`): **14/14** |
| 15:10 | C | `verify_entity` cableado al agente (stub y real) | Verde | Detecta empresa/RUC en el mensaje libre y llama `verify_entity` antes de proponer el campo relacionado — verificado por HTTP real contra el caso de demo completo |
| 2026-09-12 | B | Backend con claves reales (`main.py`, `agent.py`) | Verde (pasada 3) | 5 defectos del camino real corregidos (ver "Verificación con claves reales"). Suite 44 → **46**. E2E por HTTP 6/6 con `gpt-4o-mini` + Exa |
| 2026-09-12 | C | `extension/run-benches.mjs` | Verde | Runner comiteado para los dos bancos jsdom (antes solo existía en la máquina de quien los corrió). 20/20 + 15/15 |
| 2026-09-12 | — | Repo público | Verde | `Shine299/Agents-thinker` existe y es el `origin` — fila de Sprint-01 cerrada |

*(Sprint-01 cerrado en solitario — sin equipo de 4, secuencia A→pero ejecutado C→A→B→D según el plan aprobado. Sprint-02 fusionó la conexión real panel↔backend, originalmente prevista para Sprint-03: no tiene sentido simular un mock cuando el backend real ya funciona, en un proyecto de una sola persona. Ver `.sprints/SPEC-01.md` y `.sprints/SPEC-02.md` para las bitácoras Rojo→Verde completas.)*

## Pre-existente vs. construido durante el evento (elegibilidad)

| Elemento | Tipo | Detalle |
| --- | --- | --- |
| OpenAI Agents SDK | Librería permitida | Provee el agent loop y el tool calling; el prompt de sistema, las 2 herramientas de Sprint-01 (`read_page`, `fill_field`) y su lógica de negocio se escriben hoy en `backend/agent.py`/`tools.py` |
| Estructura de manifest MV3 | Patrón de plantilla estándar de Chrome | El indexado del DOM (`indexPage()`), `labelFor()` con fallbacks, y el puente del service worker son código nuevo del evento |
| Exa API | Servicio de sponsor | La herramienta `verify_entity` está escrita y **cableada al agente** (stub determinista + camino real vía `exa_py`, import perezoso). Clave real activa desde 2026-09-12: verificada contra el caso de demo |
| Capa i18n (`t()`, `en.json`, `es.json`) | Construido hoy | Implementación propia de ~30 líneas en `extension/i18n/index.js`, sin librería externa; paridad de claves certificada por test automatizado |
| Portal clonado | **Decisión tomada:** sintético, no clon de un sitio real | Construido íntegramente hoy (`portal-demo/mesa-partes.html`) con fealdad deliberada (tablas anidadas, IDs `ctl00_cphMain_*`, sin `<label for>`) en vez de `Save page as → Complete` sobre un portal real — ver justificación abajo |
| Backend `stub` (`VENTANA_AGENT_BACKEND=stub`) | Construido hoy, temporal | Agente determinista sin llamadas de red, para certificar Verde antes de canjear la clave de OpenAI (R8). Debe desaparecer o quedar solo como respaldo documentado antes de Sprint-03 |

*Actualizar esta tabla apenas se tome cada decisión — no reconstruir la explicación al final.*

### Decisión: portal sintético en vez de clon real (13:15)

Se evaluaron 3 opciones para `portal-demo/`: (1) generarlo sintético con fealdad garantizada, (2) que C clone un portal real con `Save page as → Complete`, (3) ambos. Se eligió **(1) sintético**, por:
- R2 de `docs/RIESGOS.md` ya señala el clon local como mitigación nº1 frente a un sitio real cayéndose; un `Save as` sobre un portal real real trae además CSS roto y JS a dominios muertos — riesgo de depurar el clon en vez del producto.
- Permite **garantizar** los patrones exactos que hacen valiosa la cadena de `labelFor()` (campos sin `<label for>`, IDs crípticos, `<td>` previo como única pista) en vez de esperar encontrarlos por suerte en un sitio real.
- El clon de un portal real queda documentado como mejora opcional (guía M6 del plan de Sprint-01), nunca bloqueante.

## Auditoría de Sprint-01 (14:00) — pasada 1 RECHAZADA

Se auditó el sprint ya declarado "Verde" y **no pasó**. Vale registrarlo porque el patrón se repite bajo presión de reloj.

**Fallos de proceso (los graves):**

| # | Hallazgo |
| --- | --- |
| A1 | La bitácora de `SPEC-01.md` **afirmaba un ciclo Rojo→Verde que nunca ocurrió**. El código se escribió antes que los tests. Violación de la regla 2 de `AGENTS.md`, y la bitácora decía lo contrario de lo ocurrido |
| A2 | Se marcó `[x]` la casilla "el repo público existe" **sin que existiera repo**, con una nota aclaratoria al lado — la forma exacta de mentir en un checklist |
| A3 | Dos "PASS" del banco de pruebas eran **aserciones vacuas**: comprobaban `7 <= 150` y `~800 <= 6144` sobre un fixture de 7 elementos. Los topes de R5 estaban sin verificar |

**Defectos funcionales encontrados:**

| # | Defecto | Por qué no se detectó |
| --- | --- | --- |
| B1 | El agente real **siempre devolvía cero acciones**: la tool descartaba su valor de retorno y la lista de propuestas nunca recibía un `append` | Los tests solo corrían en modo `stub`; el camino real no tenía ni un test |
| B2 | El `locale` **nunca llegaba al modelo**: el prompt le pedía leer un campo `locale` que no recibía | Ídem — en stub el idioma sale de un diccionario, así que el DoD "responde en inglés" pasaba sin probar nada real |
| B3 | El timeout devolvía `HTTPException(504)` — una forma JSON que **no es `TurnResponse`** y que el panel no sabe parsear. Violación directa del contrato congelado | Ningún test cubría el camino de error |
| B4 | `reply="model_error"` mostraba un **código técnico crudo al usuario**, contra `I18N_POLICY.md` §4 | Ídem |

**Lección de fondo:** un backend `stub` cómodo hizo que la suite pasara en Verde mientras el camino real estaba roto en dos sitios distintos. El default de `VENTANA_AGENT_BACKEND` era `"stub"`, así que *producción mockeaba en silencio*. Cambiado a real por defecto, con test que lo bloquea (`test_agent_backend_defaults_to_the_real_model_not_the_stub`).

**Corrección estructural aplicada:** se introdujo `tools.TurnContext`, y el `append` de la propuesta vive **dentro** de `fill_field`. Stub y camino real llaman a la misma función, así que B1 ya no puede repetirse por construcción — no depende de que alguien recuerde hacer el `append`.

## Auditoría de Sprint-02 (14:20) — pasada 1 RECHAZADA

Mismo patrón que Sprint-01: "Verde" autodeclarado tras implementar todo el alcance de `.sprints/SPEC-02.md`, y una auditoría estricta posterior encontró que dos piezas no estaban realmente terminadas — construidas, pero no verificadas de punta a punta.

**Hallazgo grave 1 — código muerto disfrazado de completo:** `verify_entity` existía en `tools.py`, tenía sus propios tests, y pasaba en Verde... pero **ninguna función que arma el agente lo registraba como herramienta**. Ni `_run_stub` ni `build_agent_tools` lo incluían. El Escenario 4 completo (verificación externa vía Exa) estaba, de hecho, incumplido — el DoD del caso de demo ("1 dato verificable por Exa") no era operativo pese a que el archivo `demo-case.txt` sí lo mencionaba. Se detectó con `grep verify_entity agent.py tools.py`: cero resultados fuera de su propia definición.

**Hallazgo grave 2 — bug de estado reproducido con datos reales:** al aprobar 1 de 3 campos propuestos, el backend respondía `status: "done"` / *"listo, completado"* mientras 2 campos seguían vacíos. Causa: `run_turn` decidía `status`/`reply` mirando solo las acciones de *ese* turno, sin consultar si `session.proposed` aún tenía propuestas de turnos anteriores sin resolver. Reproducido por HTTP real antes de tocar el código, no solo en teoría.

**Hallazgo menor:** `error.refNotFound` definida en ambos diccionarios i18n, **nunca referenciada** por `panel.js` — el diseño real centraliza los mensajes de error en el backend (`ERROR_REPLIES`/`EXHAUSTED_REPLIES`), así que la clave quedó como contenido muerto. Al revisar esto se encontraron **3 claves muertas más** (`action.approved`, `trace.retry`, `state.done`) que nadie había verificado.

**Gap de cobertura:** 35 tests de backend y 19 checks de `content.js`, pero **cero tests de `panel.js`** — exactamente el tipo de laguna que en Sprint-01 escondió bugs reales.

Veredicto pasada 1: **RECHAZADO.**

### Correcciones aplicadas (pasada 2, TDD real)

- **`verify_entity` cableado:** el stub detecta empresa (sufijo SAC/SRL/EIRL/SA) o RUC (11 dígitos) en el mensaje libre y llama `verify_entity` **antes** de cualquier `fill_field` — orden verificado en el `trace`. El camino real registra `verify_entity` como tercera tool del SDK, con `name_override="verify_entity"` (el nombre del contrato, no el identificador Python — mismo principio ya aplicado a `read_page`/`fill_field` en Sprint-01).
- **Bug de "done" prematuro corregido:** se centralizó la decisión de `status`/`reply` en `_status_for()`/`_reply_for()`, que consultan `session.proposed` (no solo `ctx.actions` de este turno). Nueva categoría de respuesta: `STILL_PENDING_REPLIES` ("N campo(s) más siguen a la espera de tu aprobación").
- **`discardAction` en el panel ahora avisa al backend** (`error: "discarded"`, un valor libre del campo `Optional[str]` que el contrato ya tenía — no se tocó la forma del JSON). Sin esto, un campo descartado quedaba huérfano en `session.proposed` para siempre y el turno nunca llegaba a `"done"`.
- **3 claves i18n muertas puestas en uso real** en vez de solo documentadas: `state.loading` (indicador durante las llamadas de red), `action.approved` (marca visual transitoria en la fila mientras se espera la respuesta del backend), `trace.retry` (etiqueta del paso de reintento en el log). `error.refNotFound`, `error.timeout` y `state.done` se **eliminaron** por no tener un uso honesto dado que el diseño ya centraliza esos mensajes en el backend.
- **Guardarraíl nuevo:** `test_no_dead_i18n_keys` falla si una clave existe en el diccionario pero ningún archivo de `extension/` la referencia — para que esta clase de deuda no vuelva a pasar desapercibida.
- **Cobertura de `panel.js` desde cero:** `extension/test-panel.html`, banco de pruebas vía jsdom con mocks completos de `chrome.tabs`/`chrome.storage`/`fetch`, reutilizando el DOM real de `panel.html`. Verifica: estabilidad del `session_id` a través del cambio de idioma, forma exacta de la petición POST, que aprobar ejecute y reporte `ok:true`, que descartar **nunca** llame `EXECUTE_ACTIONS` y reporte `error:"discarded"`, y que el log de traza se acumule entre turnos.

**Lección de fondo, repetida de Sprint-01 con una variante nueva:** no basta con "cada camino que el stub sustituye necesita un test del real" — hace falta además **un test que efectivamente invoque el flujo completo**, no solo la función aislada. `verify_entity` tenía tests propios en Verde y aun así estaba desconectado; los tests unitarios de una pieza no prueban que esa pieza esté *enchufada*.

## Verificación con claves reales (2026-09-12) — pasada 3 de Sprint-02

Con las claves puestas, el camino real falló de 5 formas distintas. **Ninguna era detectable en `stub`**, y las dos primeras ni siquiera eran detectables sin una clave con crédito. Es la tercera vez que el patrón se repite: el stub certifica el contrato, no el producto.

| # | Defecto | Cómo se vio | Corrección | Test |
| --- | --- | --- | --- | --- |
| C1 | `backend/.env` **nunca se cargaba**: `python-dotenv` estaba en `requirements.txt` sin que nadie llamara `load_dotenv()` | Las claves puestas no tenían efecto | `load_dotenv(Path(__file__).with_name(".env"))` en `main.py` | Manual (`EXA_API_KEY=probe` → cargado) |
| C2 | `read_page_tool` devolvía al modelo `"4 elements available"` — **el modelo nunca veía refs ni labels** y los inventaba (`contact_name`, `ruc`) → `ref_not_found` en cadena | `trace` de la primera corrida real | La tool devuelve el índice JSON compacto (`exclude_none`, `exclude_defaults`) | `test_read_page_tool_shows_the_model_every_ref_and_label` |
| C3 | El modelo **ni llamaba `read_page`** antes de proponer: iba directo a `fill_field` | Ídem | Índice inyectado en el input del turno (`build_turn_input`); `read_page` queda como tool para la relectura tras `ref_not_found` | `test_turn_input_carries_the_page_index_and_the_user_message` |
| C4 | Modelo por defecto del SDK (`gpt-5.6-luna`, razonador): **11s por turno** > 8s del contrato | `timeout after 8s` | `DEFAULT_MODEL = "gpt-4o-mini"` (override con `VENTANA_MODEL`). Timeout 8 → 20s: el caso de demo real de 10 campos tarda 7.6–10.5s | Medido, 6/6 corridas |
| C5 | Prompt: decía "he llenado" sin aprobación; `gpt-4.1-mini` respondía en ES con `locale: "en"`; pasaba el correo entero a `verify_entity`; y **vetaba** la propuesta cuando Exa devolvía un RUC distinto | Corridas reales 2 modelos × 2 idiomas | Prompt afinado: refs exactos, tanda única de `fill_field`, "propone y espera aprobación", locale estricto, **verificación informativa, no veto** (la discrepancia va al `reason`) | 6/6 corridas reales |

**Decisión sobre el caso de demo:** el RUC `20456789123` de `demo-case.txt` es ficticio; Exa encuentra "EXPORT IMPORT & GRUPO ANDINO SAC – 20539177398". Se mantiene el ficticio a propósito: el agente propone el valor del correo y anota en el `reason` que la verificación externa devolvió otro RUC — es el momento más vendible del video ("el agente lo detectó, y aun así la decisión es tuya").

**Decisión de modelo:** `gpt-4o-mini` sobre `gpt-4.1-mini`. Con el mismo prompt, 4o-mini respeta el orden `verify_entity` → `fill_field`, respeta el `locale` y pone la discrepancia del RUC en el `reason`; 4.1-mini verificaba al final y en una corrida ignoró el locale.

## Lecciones aprendidas

- **Tercera repetición del patrón stub:** las claves reales sacaron 5 defectos, y dos de ellos (C2, C3) hacían el producto **inservible** — el modelo no podía citar un solo ref válido — mientras 44 tests y 34 checks estaban en verde. Regla nueva, además de las dos anteriores: **ninguna fila del backlog que dependa del modelo se marca Done sin al menos una corrida con clave real registrada en la bitácora.** Un stub certifica el contrato, no el producto.
- **El timeout del contrato se calibró sin medir.** 8s era un número razonable para un stub; un modelo real con 11 tool calls necesita 8–10s. Medir antes de congelar.

- **`openai-agents` NO importa en Python 3.9 — y esta máquina tiene 3.9.6, no 3.11+.** Corrección de una nota anterior de esta misma bitácora, que decía que "instaló y corrió sin problema": **instaló, pero fallaba al importar en runtime** (`TypeError: Unable to evaluate type annotation 'float | None'`, sintaxis de unión de 3.10+ dentro del SDK). No se detectó antes porque **solo se había ejecutado el modo `stub`**, que nunca importa el SDK. Es exactamente el fallo que `docs/PREPARACION_PREVIA.md` manda descubrir antes de las 11:15 ("una llamada real a la API verificada"). Resuelto añadiendo `eval_type_backport` a `requirements.txt` (inofensivo en 3.11+). **Si hay tiempo, instalar Python 3.11+ igualmente** — es lo que pide `TECH_STACK.md` y evita más sorpresas del SDK.
- **Los dos topes del contrato no son independientes: el de 6 KB satura mucho antes que el de 150 elementos.** Medido: 400 campos se recortan a **59**, no a 150, porque el esqueleto JSON de cada elemento (~95 bytes) hace que 150 elementos pesen ~14 KB. En la práctica el índice nunca pasará de ~60 elementos. Irrelevante para el portal de demo (12 campos), pero **un portal legado real con 200 campos perdería la mayoría**, y el agente no vería los campos recortados. No se cambió la forma del payload porque el contrato está congelado desde las 11:15; queda como riesgo abierto para Sprint-02 (opción barata: omitir claves nulas/`false` al serializar, que casi duplica los campos que caben).
- **Nombres de herramienta visibles al modelo.** El SDK toma el nombre de la función Python (`fill_field_tool`), no el del contrato. Se forzó `name_override="fill_field"` para que el modelo vea exactamente los nombres de `docs/API_CONTRACTS.md`. Sin esto, el prompt habla de `fill_field` y el modelo recibe otra cosa.
- **`CSS.escape()` no es universal** — se descubrió al validar `labelFor()` con jsdom (que no lo implementa). Se reemplazó `querySelector('label[for="..."]')` con `CSS.escape` por una iteración manual sobre `label[for]` comparando `label.htmlFor === el.id`. Más robusto además para IDs de portales legados con caracteres especiales (`ctl00$cphMain$...`) — se mantiene así aunque corra en Chrome real, no solo por el test.
- **La cadena de fallback de `labelFor()` favorece `placeholder` sobre el texto del `<td>` previo**, tal como especifica `DOMAIN.md`. Verificado con un caso real: el campo de email resolvió a `"correo@ejemplo.com"` (su placeholder) en vez de `"Correo electronico"` (el `<td>` anterior) — es el comportamiento correcto según el orden documentado, no un bug, pero conviene decirlo en el video con un ejemplo donde el placeholder sea menos informativo que el label real.
- **Elementos no formularios (`<button>`) heredan el fallback de "hermano previo"** de forma un poco rara: un botón sin texto propio capturado puede terminar con el texto del botón anterior como `label` (ej. "Enviar Solicitud" resolvió a `"Limpiar"`, el texto del botón previo). Sin impacto en Sprint-01 (no hay herramienta de envío, los botones no son destino de `fill_field`), pero si se decide indexar el propio `textContent` del elemento como último fallback, hacerlo en Sprint-02 con un test dedicado.
- **`asyncio.wait_for` + `asyncio.to_thread`** en `main.py` implementa el timeout duro de 8s del contrato sin bloquear el loop de FastAPI — barato y suficiente para Sprint-01/02.
- **El backend `stub` es un arma de doble filo.** Permitió certificar en Verde sin clave de OpenAI (el caso que R8 anticipa), pero ocultó dos bugs del camino real durante todo un sprint. Regla adoptada: **todo camino que el stub sustituye necesita al menos un test que ejercite el real** — aunque sea sin red, verificando el cableado (`build_agent_tools`, `build_instructions`, nombres de herramienta).
- **Ruta de respaldo OpenRouter implementada y probada** (R8): si falta `OPENAI_API_KEY` y existe `OPENROUTER_API_KEY`, se redirige el cliente sin refactor. OpenAI gana si están las dos. El proveedor elegido se anota en el `trace`, para que el cambio sea visible y no silencioso.
- **jsdom (el que usan los bancos de pruebas vía Node) no implementa `fetch`.** El primer intento de `extension/test-panel.html` intentaba hacer *passthrough* al `fetch` real para los JSON de `i18n/`, y reventaba con `Cannot read properties of undefined`. Solución: inyectar los diccionarios reales leídos del disco vía la opción `beforeParse` de `JSDOM.fromURL` (`window.__i18nFixtures`), en vez de depender de un `fetch` que no existe en ese entorno — así el mock nunca necesita red ni un passthrough real, y el test bench sigue reflejando el contenido real de los diccionarios, no una copia a mano.
- Resultado de cada punto de decisión (12:30 y 14:30): Punto de Decisión 1 → **Verde** (ver fila de la tabla de estado). Punto de Decisión 2, aún no se llega a esa hora del cronograma.

## Fuera de alcance (explícito, no silencioso)

| Elemento | Motivo |
| --- | --- |
| Auth0 | No refuerza la tesis de "sesión ya autenticada del usuario"; costo de 40-60 min no rentable hoy |
| Despliegue en Google Cloud Run | No suma puntos de rúbrica en un evento de un día; queda documentado como plan futuro |
| Flujo 2 (lectura de tabla) y Flujo 3 (revisión previa al envío) | Se construyen solo si el Flujo 1 está cerrado y estable — prioridad estricta |
| Base de datos persistente | Estado en memoria por `session_id` alcanza para la demo y el video |
| Bundler / React / Vite / webpack en la extensión | Un paso de build es un punto de fallo adicional; JS plano evita 20 min de riesgo |
