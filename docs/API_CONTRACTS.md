# API_CONTRACTS.md

**Estado: CONGELADO a las 11:15. No se toca durante el resto del build.**
Este es el único acuerdo que A (extensión) y B (agente) necesitan para trabajar en paralelo con mocks sin bloquearse.

---

## Endpoints

| Método | Ruta | Para qué | Frente responsable |
| --- | --- | --- | --- |
| `GET` | `/health` | Verificación de que el backend vive. Lo primero que prueba la extensión al abrir el panel | B |
| `POST` | `/agent/turn` | Único endpoint de trabajo. Maneja tanto el mensaje inicial como el retorno de resultados de acciones | B |

## `POST /agent/turn` — request

```json
{
  "session_id": "s_8f2a",
  "locale": "es",
  "message": "Llena el formulario con este correo: ...",
  "page": {
    "url": "http://localhost:5500/mesa-partes.html",
    "title": "Registro de solicitud",
    "elements": [
      {
        "ref": "e12",
        "tag": "input",
        "type": "text",
        "label": "Nombre del solicitante",
        "value": "",
        "options": null,
        "required": true
      }
    ]
  },
  "action_results": null
}
```

| Campo | Tipo | Obligatorio | Nota |
| --- | --- | --- | --- |
| `session_id` | string | sí | Lo genera el panel al abrirse. Mantiene el historial de la conversación |
| `locale` | enum (`"es"` \| `"en"`) | sí | Idioma en que el agente debe redactar `reply` y cada `reason`. Ver `docs/I18N_POLICY.md` |
| `message` | string \| null | no | Va en `null` cuando el turno solo devuelve resultados de acciones |
| `page` | objeto \| null | sí en el primer turno | Snapshot del DOM indexado. Se reenvía en cada turno porque la página cambia |
| `page.elements` | arreglo | sí | Máximo 150 elementos, ≤6 KB serializados. Nunca HTML crudo |
| `action_results` | arreglo \| null | no | Resultado de las acciones que el usuario aprobó en el turno anterior |

## `POST /agent/turn` — response

```json
{
  "session_id": "s_8f2a",
  "status": "awaiting_approval",
  "reply": "Encontré 8 campos que puedo llenar con los datos del correo.",
  "actions": [
    {
      "action_id": "a1",
      "tool": "fill_field",
      "args": { "ref": "e12", "value": "Juan Pérez Quispe" },
      "needs_approval": true,
      "reason": "Campo «Nombre del solicitante», tomado del remitente del correo"
    }
  ],
  "trace": [
    { "step": 1, "tool": "read_page", "outcome": "ok, 43 elementos" },
    { "step": 2, "tool": "verify_entity", "outcome": "ok, empresa encontrada" }
  ]
}
```

| Campo | Tipo | Nota |
| --- | --- | --- |
| `status` | enum | `awaiting_approval` · `done` · `error` |
| `reply` | string | Lo que el panel muestra como texto del agente. **Redactado en el `locale` de la petición** |
| `actions` | arreglo | Vacío cuando `status` es `done`. Cada acción se pinta como fila con botón de aprobar |
| `action_id` | string | Identificador del turno. El panel lo devuelve en `action_results` |
| `reason` | string | Se muestra en la UI — convierte la aprobación en decisión informada, no en clic ciego. **Redactado en el `locale` de la petición** |
| `trace` | arreglo | Pasos dados por el agente. Se pinta en el log del panel |

## Retorno de resultados (segunda vuelta)

```json
{
  "session_id": "s_8f2a",
  "locale": "es",
  "message": null,
  "page": { "...snapshot nuevo..." },
  "action_results": [
    { "action_id": "a1", "ok": true,  "value": "Juan Pérez Quispe", "error": null },
    { "action_id": "a2", "ok": false, "value": null, "error": "ref_not_found" }
  ]
}
```

## Herramientas (contrato interno del agente)

| Herramienta | Entrada | Salida | Nota |
| --- | --- | --- | --- |
| `read_page` | — | índice de elementos + título + URL | Se llama al inicio y tras cada acción que cambie la página |
| `fill_field` | `ref`, `value` | ok / error con motivo | Pasa por aprobación. Dispara `input` y `change` con `bubbles: true` |
| `extract_table` | `ref` de la tabla | filas como arreglo de objetos | Detecta encabezados; corta a 200 filas |
| `verify_entity` | `query` | resultado de Exa | Valida datos externos (empresa, dirección) |

## Códigos de error de herramienta

| Código | Significado | Qué hace el agente |
| --- | --- | --- |
| `ref_not_found` | El elemento ya no está en el DOM | Re-ejecuta `read_page` una vez y reintenta con el índice nuevo |
| `element_not_visible` | Existe pero está oculto o deshabilitado | Lo reporta al usuario, no reintenta |
| `page_stale` | La URL cambió entre el plan y la ejecución | Descarta el plan completo y vuelve a empezar |
| `tool_timeout` | El content script no respondió en 3s | Reporta y detiene el turno |
| `model_error` | Fallo de la API del modelo | El backend responde `status: "error"` con mensaje legible |

**Regla dura: un solo reintento por acción, nunca en bucle, nunca fallar en silencio.**

## Protocolo interno de la extensión (`chrome.runtime`)

| Mensaje | Origen → destino | Payload |
| --- | --- | --- |
| `INDEX_PAGE` | panel → content | — → `{ url, title, elements[] }` |
| `EXECUTE_ACTIONS` | panel → content | `{ actions: [...] }` → `{ action_results: [...] }` |
| `PING` | panel → content | Verifica que el content script esté inyectado |

## Reglas no negociables del contrato

- Timeout de `/agent/turn`: **20 segundos** (era 8, calibrado sobre el stub; el caso de demo de 10 campos con modelo real tarda 7.6–8.3s — solo cambió el valor, no la forma).
- `page.elements` no pasa de 150 entradas ni de 6 KB serializados.
- El indexado **excluye todo `input[type="password"]`**.
- Ninguna acción con `needs_approval: true` se ejecuta sin clic del usuario. No hay "modo automático".
- La herramienta de envío **no existe** — no está deshabilitada, no está implementada.
- `locale` es **obligatorio** en cada petición. El backend nunca adivina el idioma a partir del `message`.
- Los códigos de error (`ref_not_found`, `page_stale`, …) son identificadores técnicos y **nunca se traducen**. Se traduce solo su presentación en el panel, vía las claves `error.*` de `extension/i18n/`.
- Los `label` de los campos del formulario y los `ref` se citan **textualmente**, en el idioma original del portal. El agente nunca los traduce dentro de un `reason`.
