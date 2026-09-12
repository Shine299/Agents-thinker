# I18N_POLICY.md

**Norma de proyecto, vinculante bajo SDD.** Ningún SPEC se certifica en Verde si viola esta política. El Supervisor TDD la verifica en cada transición Rojo→Verde.

---

## 1. Regla de oro

| Capa | Idioma | Por qué |
| --- | --- | --- |
| **Código, identificadores, comentarios, commits, nombres de archivo** | **Inglés, siempre** | El repo es público y lo evalúa un jurado global. Código mezclado (`llenarCampo`, `// verifica si existe`) delata improvisación y penaliza el criterio C |
| **README.md y toda la documentación del repositorio público** | **Inglés** | Es lo primero que abre el jurado después del video |
| **Interfaz del producto (side panel)** | **Bilingüe ES / EN, seleccionable en runtime** | El usuario final es un trabajador administrativo en LATAM; el evaluador es global. Ambos tienen que poder usarlo |
| **Respuestas del agente (`reply`, `reason`, mensajes de error)** | **En el idioma activo del usuario** | Generadas por el modelo, así que el idioma viaja en la petición |
| **Documentación interna de metodología** (`.sprints/`, `docs/RETO_*`, `docs/ESTRATEGIA_*`, `docs/RIESGOS.md`, `docs/PREPARACION_PREVIA.md`, `docs/GUION_VIDEO.md`) | **Español** | Es documentación de trabajo del equipo durante 4h15. Traducirla cuesta tiempo y no la lee el jurado |

**Excepción única:** `docs/API_CONTRACTS.md` y `DOMAIN.md` usan nombres técnicos en inglés (endpoints, campos, herramientas, códigos de error) con explicaciones en español. Los nombres son el contrato; las explicaciones son para el equipo.

## 2. Nada de texto embebido en el código

Prohibido en cualquier archivo de `extension/` o `backend/`:

```js
// PROHIBIDO
panel.textContent = "Campos detectados";
return { error: "No se encontró el elemento" };
```

Todo string visible al usuario sale de un diccionario de traducción:

```js
// CORRECTO
panel.textContent = t('page.elementsDetected', { count: n });
```

## 3. Estructura de los diccionarios

```
extension/
  i18n/
    en.json
    es.json
    index.js        # t(key, params) + detección y persistencia de locale
```

**Formato de clave:** `dominio.concepto` en `camelCase`, en inglés. Nunca la frase como clave.

```json
// en.json
{
  "panel.title": "Ventana",
  "panel.connected": "Connected",
  "panel.disconnected": "Not connected",
  "input.placeholder": "Paste the email or request text here",
  "input.submit": "Fill form",
  "page.elementsDetected": "{count} fields detected on this page",
  "page.noPasswords": "Password fields are never indexed",
  "action.approve": "Approve",
  "action.discard": "Discard",
  "action.approved": "Approved",
  "trace.title": "Agent steps",
  "trace.retry": "retry",
  "state.loading": "Working…",
  "state.empty": "No actions proposed yet",
  "state.done": "{count} fields filled. Review and submit the form yourself.",
  "error.backendUnreachable": "Cannot reach the local agent. The panel is still active; you can retry.",
  "error.refNotFound": "That field is no longer on the page. The agent re-read it and retried.",
  "error.timeout": "The agent took too long to respond. Nothing was changed on the page."
}
```

```json
// es.json
{
  "panel.title": "Ventana",
  "panel.connected": "Conectado",
  "panel.disconnected": "Sin conexión",
  "input.placeholder": "Pega aquí el correo o el texto de la solicitud",
  "input.submit": "Llenar formulario",
  "page.elementsDetected": "{count} campos detectados en esta página",
  "page.noPasswords": "Los campos de contraseña nunca se indexan",
  "action.approve": "Aprobar",
  "action.discard": "Descartar",
  "action.approved": "Aprobado",
  "trace.title": "Pasos del agente",
  "trace.retry": "reintento",
  "state.loading": "Trabajando…",
  "state.empty": "Aún no hay acciones propuestas",
  "state.done": "{count} campos llenados. Revisa y envía tú el formulario.",
  "error.backendUnreachable": "No pude contactar al agente local. El panel sigue activo; puedes reintentar.",
  "error.refNotFound": "Ese campo ya no está en la página. El agente la releyó y reintentó.",
  "error.timeout": "El agente tardó demasiado en responder. No se modificó nada en la página."
}
```

**Regla dura:** `en.json` y `es.json` tienen **exactamente el mismo conjunto de claves**. Una clave presente en uno y ausente en el otro es un fallo de test, no una advertencia.

## 4. Idioma de las respuestas del agente

`reply`, `reason` y los mensajes de error que genera el modelo no se pueden traducir con un diccionario — el modelo los escribe. Por eso el `locale` viaja en cada petición a `/agent/turn` y el prompt de sistema del backend lo respeta:

```
Respond in the language given by the `locale` field of the request:
"es" -> Spanish, "en" -> English. Never mix languages inside one reply.
This applies to `reply` and to every `reason` in `actions`.
```

**Lo que NO se traduce nunca**, ni siquiera en el `reply`:
- Los `label` de los campos del formulario (vienen del portal legado, se citan textualmente).
- Los `ref` (`e12`).
- Los códigos de error del contrato (`ref_not_found`, `page_stale`): son identificadores técnicos; solo su *presentación* al usuario se traduce, vía `error.refNotFound`.

## 5. Selección y persistencia del idioma

1. Al abrir el panel por primera vez, se toma `chrome.i18n.getUILanguage()`. Si empieza por `es` → `es`; en cualquier otro caso → `en`.
2. Un selector `ES / EN` en la cabecera del panel permite cambiarlo en cualquier momento.
3. La elección se guarda en `chrome.storage.local` y sobrevive al cierre del panel.
4. Cambiar de idioma **no reinicia la sesión**: el historial se conserva, solo cambian los textos de interfaz y el idioma de las respuestas siguientes.

## 6. Qué verifica el Supervisor TDD

| Chequeo | Cuándo |
| --- | --- |
| Cero strings visibles hardcodeados en `extension/` y `backend/` | En cada certificación Verde |
| `en.json` y `es.json` con claves idénticas (test automatizado) | En cada certificación Verde |
| Todo identificador, comentario y mensaje de commit en inglés | En cada certificación Verde |
| El agente responde en el `locale` recibido, sin mezclar idiomas | Sprint-02 en adelante |
| El README público está íntegramente en inglés | Punto de Decisión 2 (14:30) |

## 7. Argumento para el jurado

Esto no es cosmética. En el video, la frase que lo convierte en puntos:

> "The portals are in Spanish. The people using them work in Spanish. The agent speaks their language — and it speaks yours."

Cambiar el idioma en vivo, durante la demo, cuesta dos segundos y demuestra que el producto está pensado para su usuario real, no solo para la evaluación. Es criterio **D** (utilidad y adecuación al entorno) casi gratis.
