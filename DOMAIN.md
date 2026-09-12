# DOMAIN.md

## Glosario del dominio

| Término | Definición |
| --- | --- |
| **Portal legado** | Sistema administrativo sin API (mesa de partes, intranet, ERP antiguo) donde el trabajo ocurre en la práctica |
| **Índice de página** | Representación compacta (JSON, ≤150 elementos, ≤6 KB) de los elementos accionables del DOM, producida por `indexPage()` |
| **`ref`** | Identificador estable (`e0`, `e1`, ...) asignado a cada elemento interactivo del DOM en el momento del indexado |
| **`label`** | Texto humano asociado a un elemento, resuelto por `labelFor()` con la cadena de fallbacks: `<label for>` → `aria-label` → `placeholder` → texto del `<td>` anterior → texto del nodo hermano previo |
| **Acción** | Propuesta del agente para modificar la página (ej. `fill_field`), con `reason` visible y `needs_approval` |
| **Aprobación** | Confirmación explícita del usuario, fila por fila, antes de que una acción se ejecute sobre el DOM real |
| **Turno** | Un ciclo completo de `POST /agent/turn`: entrada (mensaje o resultados de acciones) → salida (reply + actions + trace) |
| **`trace`** | Registro de los pasos que dio el agente en un turno (qué herramienta, con qué resultado); se pinta en el log del panel |
| **Reintento único** | Política de recuperación: ante `ref_not_found`, el agente re-lee la página una vez y reintenta; si falla de nuevo, se detiene y lo reporta |
| **Verificación externa** | Consulta a Exa vía `verify_entity` para confirmar que un dato (empresa, dirección) existe realmente |
| **Sesión** | Contexto identificado por `session_id`, mantenido en memoria en el backend mientras el proceso corre |
| **`locale`** | Idioma activo de la sesión (`"es"` o `"en"`). Viaja en cada petición y determina en qué idioma redacta el agente `reply` y `reason` |
| **Clave de traducción** | Identificador `dominio.concepto` en `camelCase` inglés que resuelve a un texto visible vía `t()`. Nunca se usa la frase como clave |

## Convenciones de nomenclatura

| Ámbito | Convención | Ejemplo |
| --- | --- | --- |
| Endpoints | `snake_case` en la ruta, verbo implícito por método HTTP | `/agent/turn`, `/health` |
| Campos JSON | `snake_case` | `session_id`, `action_results`, `needs_approval` |
| Herramientas | `snake_case`, verbo + objeto | `read_page`, `fill_field`, `extract_table`, `verify_entity` |
| Referencias de elementos DOM | `e` + índice numérico | `e0`, `e12`, `e43` |
| Códigos de error | `snake_case` descriptivo del fallo | `ref_not_found`, `element_not_visible`, `page_stale`, `tool_timeout`, `model_error` |
| Estados de turno | enum en minúsculas | `awaiting_approval`, `done`, `error` |
| Mensajes internos de extensión | `SCREAMING_SNAKE_CASE` | `INDEX_PAGE`, `EXECUTE_ACTIONS`, `PING` |
| Claves de traducción | `dominio.concepto` en `camelCase`, en inglés | `action.approve`, `page.elementsDetected`, `error.refNotFound` |
| Códigos de idioma | ISO 639-1 en minúsculas | `es`, `en` |
| Identificadores de código, comentarios y commits | **Inglés siempre** | `fillField()`, `// retry once after ref_not_found` |

Todo `SPEC.md`, todo endpoint y toda variable de dominio debe usar exactamente estos nombres — no sinónimos.

**Nota de idioma.** Los términos de este glosario se explican en español porque son documentación de trabajo del equipo, pero sus **nombres técnicos son inglés y son el contrato**: en el código nunca aparece `llenarCampo` ni `referencia`, siempre `fillField` y `ref`. Ver `docs/I18N_POLICY.md`.
