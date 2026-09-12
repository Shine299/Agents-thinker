# BACKLOG.md

4 sprints dentro de la ventana real 11:15–15:30. El Supervisor TDD preside los 2 puntos de decisión (12:30 y 14:30); solo él puede marcar una fila como "Done".

| ID Sprint | Horario | Épica | Frente | Criterio rúbrica | Estado | DoD (verificable) |
| --- | --- | --- | --- | --- | --- | --- |
| Sprint-00 | 10:00–11:15 | Preparación previa: encuesta de créditos + setup verificado por persona (ver `docs/PREPARACION_PREVIA.md`) | A, B, C, D | Habilitante | Pendiente | Los 5 checks de la tabla por persona en Verde antes de las 11:15 |
| Sprint-00 | 11:00–11:15 | Congelar idea, stack y contrato `/agent/turn` | Todos | A | Pendiente | `docs/API_CONTRACTS.md` declarado congelado en voz alta, con el equipo completo |
| Sprint-01 | 11:15–12:00 | Extensión carga, el panel abre, indexado devuelve JSON | A | A | Pendiente | `INDEX_PAGE` devuelve un índice válido (≤150 elementos) sobre el portal clonado |
| Sprint-01 | 11:15–12:00 | Agent loop respondiendo a un payload mock con `read_page` | B | A | Pendiente | `/agent/turn` responde `status: awaiting_approval` con al menos una acción propuesta, contra un mock |
| Sprint-01 | 11:15–12:00 | Portal clonado sirviendo en local (`python -m http.server 5500`) | C | A | Pendiente | El formulario real (con su fealdad estructural intacta) carga en `localhost:5500` |
| Sprint-01 | 11:15–12:00 | Repo creado, **README esqueleto en inglés**, guion v1 del video | D | Entrega | Pendiente | Repo público existe; README en inglés con secciones vacías tituladas |
| Sprint-01 | 11:30–12:00 | Andamiaje i18n: `extension/i18n/{en,es}.json` + `t(key, params)` + detección de locale | A | D | Pendiente | El panel renderiza sus textos vía `t()`; cero strings hardcodeados desde el primer commit |
| Sprint-01 | 11:30–12:00 | `locale` obligatorio en `/agent/turn` y respetado por el prompt de sistema | B | D | Pendiente | Con `locale: "en"` el agente responde en inglés; con `"es"`, en español |
| — | **12:30** | **PUNTO DE DECISIÓN 1** — si la extensión no carga y no se comunica con el backend, activar plan B (CopilotKit Channels → Slack, mismo backend) | Supervisor TDD | A | Gate | Verde/Ámbar/Rojo declarado explícitamente antes de abrir Sprint-02 |
| Sprint-02 | 12:30–13:30 | `fill_field` funcionando con eventos reales (`input`/`change`, `bubbles: true`) | A | C | Pendiente | Un campo del formulario clonado se llena solo y el portal lo reconoce como válido |
| Sprint-02 | 12:30–13:30 | `fill_field` + flujo de aprobación + reintento ante `ref_not_found` | B | C, D | Pendiente | El reintento es visible en el `trace`; ninguna acción se ejecuta sin aprobación |
| Sprint-02 | 12:30–13:30 | Caso de demo cerrado (correo ficticio) + `verify_entity` con Exa integrado | C | A, C | Pendiente | El agente detecta un dato que requiere verificación externa y la resuelve vía Exa |
| Sprint-02 | 12:30–13:30 | Selector ES/EN en la cabecera del panel, con persistencia en `chrome.storage.local` | A | D | Pendiente | Cambiar de idioma no reinicia la sesión ni pierde el historial |
| Sprint-02 | 12:30–13:30 | Mensajes de error traducidos vía claves `error.*` (el código técnico queda solo en el `trace`) | A, B | C, D | Pendiente | `ref_not_found` se muestra en el idioma activo; el código crudo nunca llega a la UI |
| Sprint-02 | 12:30–13:30 | Grabación de pantalla del avance (respaldo si algo falla después) | D | Entrega | Pendiente | Archivo de video parcial guardado |
| Sprint-03 | 13:30–14:30 | Integración real extensión ↔ backend (fin de los mocks) | A | A | Pendiente | El panel llama al backend real y pinta la respuesta real, no un mock |
| Sprint-03 | 13:30–14:30 | Prompt del sistema afinado; mensajes de error en lenguaje claro | B | C, D | Pendiente | Un `model_error` o `ref_not_found` se lee en el panel en español claro, no como stack trace |
| Sprint-03 | 13:30–14:30 | **Prueba end-to-end en bucle** sobre el flujo 1 completo | C | A | Pendiente | 3 corridas seguidas del flujo 1 sin intervención manual fuera del panel |
| Sprint-03 | 13:30–14:30 | Paridad de claves `en.json` ↔ `es.json` verificada por test automatizado | A | C | Pendiente | El test falla si una clave existe en un archivo y no en el otro |
| Sprint-03 | 13:30–14:30 | Prueba end-to-end del Flujo 1 **en los dos idiomas** | C | A, D | Pendiente | Una corrida completa en `es` y otra en `en`, sin mezcla de idiomas en ninguna respuesta |
| Sprint-03 | 13:30–14:30 | Primer corte del video con lo que haya construido hasta este punto, **incluyendo el cambio de idioma en vivo** | D | Entrega | Pendiente | Corte de video existente, aunque no sea el final |
| — | **14:30** | **PUNTO DE DECISIÓN 2 — CONGELAMIENTO ABSOLUTO DE CÓDIGO** | Supervisor TDD | A, B, C, D | Gate | Auditoría final Verde/Ámbar/Rojo por criterio; cualquier bug posterior se documenta como limitación conocida, no se arregla |
| Sprint-04 | 14:30–15:00 | Congelar código en los 4 frentes; últimas pruebas de C sin tocar lógica | A, B, C | A, B, C, D | Pendiente | Nadie escribe código de aplicación después de las 14:30 |
| Sprint-04 | 14:30–15:00 | Video final grabado (guion de 2 min) | D | Entrega | Pendiente | Video ≤2 min exportado |
| Sprint-04 | 15:00–15:30 | README final **íntegramente en inglés** (arquitectura + limitaciones conocidas), descripción, post social, **envío al portal** | D | Entrega | Pendiente | Los 5 elementos del portal completos y enviados antes de las 15:30; cero español en el README |
| Sprint-04 | 14:00–14:45 **(opcional)** | Ambiguous AI como destino del registro de acciones del agente — abre el premio dedicado (NVIDIA DGX Spark), el de menor competencia del evento | D | Premio especial | Condicional | **Solo si** D ya cerró sus tareas de entrega Y el Punto de Decisión 2 no tiene filas en Rojo. Nunca antes. No toca el proyecto principal |

**Nota de priorización si el tiempo aprieta en cualquier sprint:** A > B > C > D (funcionalidad end-to-end primero, innovación del entorno segundo, ejecución técnica tercero, pulido de experiencia cuarto). Nunca se sacrifica el envío por pulir C o D.
