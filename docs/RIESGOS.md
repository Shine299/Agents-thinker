# RIESGOS.md

Tabla viva. C y el Supervisor TDD la tienen abierta durante todo el build. Cada riesgo tiene dueño y hora de verificación — un riesgo sin hora de chequeo es un riesgo que se descubre tarde.

| # | Riesgo | Probabilidad | Mitigación | Dueño | Verificar a las |
| --- | --- | --- | --- | --- | --- |
| R1 | **Llegar a 15:30 sin enviar** | **La más alta de todas** | D trabaja en entrega desde las 11:15, no desde las 14:30. Congelamiento de código a las 14:30 sin excepción | D | 12:30 · 14:30 |
| R2 | El DOM cambia o el sitio se cae en la demo | Alta si trabajan en vivo | Portal clonado en local. Es la mitigación número uno — nunca se trabaja contra el sitio real | C | 12:00 |
| R3 | El agente no identifica los campos del formulario | Media | Invertir 20 minutos reales en `labelFor` con la cadena completa de fallbacks (`<label for>` → `aria-label` → `placeholder` → `<td>` previo → hermano previo) | A | 12:30 |
| R4 | El llenado no dispara los validadores del portal | Media | Despachar `input` y `change` con `bubbles: true` en cada escritura. Asignar `el.value = x` a secas NO activa los validadores | A | 13:00 |
| R5 | El payload de la página excede el contexto del modelo | Media | Tope de 150 elementos, `options` cortadas a 20, nunca HTML crudo. Máximo 6 KB serializados | B | 12:30 |
| R6 | Permisos MV3 mal configurados | Media | `activeTab` + `sidePanel` + `scripting` + `host_permissions` a localhost. **Probarlo a las 11:30, no a las 14:00** | A | 11:30 |
| R7 | Gastar tiempo en deploy y quedarse sin build | Media | Backend en `localhost:8000`. Nada de Docker ni Cloud Run antes de las 14:30 | B | 11:15 (decisión ya tomada) |
| R8 | El código de OpenAI se agota | Baja | Llenar la encuesta de créditos a las 10:00. OpenRouter como ruta de respaldo con el mismo formato de llamada | B | 10:00 · 13:30 |

## Riesgos de proceso (añadidos por el Supervisor TDD)

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R9 | A y B se pasan la tarde sincronizándose en vez de construir | El contrato `docs/API_CONTRACTS.md` se congela a las 11:15 y no se renegocia. Cada uno trabaja contra mocks |
| R10 | Scope creep: alguien empieza el Flujo 2 o 3 antes de cerrar el Flujo 1 | Los Flujos 2 y 3 están declarados fuera de alcance en `MEMORY.md`. Solo se abren si el Supervisor certifica el Flujo 1 en Verde |
| R11 | Se descubre a las 15:00 que no se puede explicar qué es pre-existente y qué se hizo hoy | `MEMORY.md` registra la elegibilidad desde la primera tarea, no al final |

## Plan B mayor — Punto de Decisión 1 (12:30)

Si la extensión no está cargando y comunicándose con el backend a las 12:30, se pivota a **CopilotKit Channels → Slack**: mismo backend, mismo agent loop, mismas 4 herramientas. El pivote cuesta 30 minutos *solo si* el backend nunca supo que existía una extensión — por eso el canal va desacoplado desde el primer commit y el contrato `/agent/turn` es agnóstico del transporte.

**Costo del pivote si se hizo bien:** 30 min. **Si el backend quedó acoplado a la extensión:** el proyecto no se recupera. Esta es la razón arquitectónica de la regla "cero lógica de razonamiento en el cliente".
