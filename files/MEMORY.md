# MEMORY.md

Retrospectiva continua del proyecto Ventana. Se actualiza en vivo, con hora, por ambos roles (Development Team y Supervisor TDD).

## Estado del sistema (actualizar en cada cierre de tarea)

| Hora | Frente | Componente | Estado | Nota |
| --- | --- | --- | --- | --- |
| — | A | Extensión (manifest, panel, content script) | No iniciado | — |
| — | B | Backend (`/health`, `/agent/turn`, agent loop) | No iniciado | — |
| — | C | Portal clonado + caso de demo + Exa | No iniciado | — |
| — | D | README / guion / video / entrega | No iniciado | — |

*(El Development Team llena esta tabla en vivo durante el build; esta plantilla arranca vacía a propósito.)*

## Pre-existente vs. construido durante el evento (elegibilidad)

| Elemento | Tipo | Detalle |
| --- | --- | --- |
| OpenAI Agents SDK | Librería permitida | Provee el agent loop y el tool calling; el prompt de sistema, las 4 herramientas y su lógica de negocio se escriben hoy |
| Estructura de manifest MV3 | Patrón de plantilla estándar de Chrome | El indexado del DOM, `labelFor` con fallbacks, y la ejecución de acciones son código nuevo del evento |
| Exa API | Servicio de sponsor | La herramienta `verify_entity` que la invoca se escribe hoy |
| Capa i18n (`t()`, `en.json`, `es.json`) | Construido hoy | Implementación propia de ~20 líneas, sin librería externa |
| Portal clonado | Copia de un portal real (`Save page as → Complete`) | Los datos de prueba y el caso de demo son ficticios y se preparan hoy |

*Actualizar esta tabla apenas se tome cada decisión — no reconstruir la explicación al final.*

## Lecciones aprendidas

*(se llena durante el build — ejemplos de qué tipo de entrada va aquí)*

- Decisiones de stack y por qué (ej. Python+FastAPI sobre Java: ahorro de 45-60 min de agent loop propio).
- Atajos tomados conscientemente y su costo/beneficio (ej. sin base de datos, estado en memoria por `session_id`).
- Errores encontrados y cómo se resolvieron (ej. `el.value = x` no dispara validadores del portal → hubo que despachar `input`/`change` con `bubbles: true`).
- Resultado de cada punto de decisión (12:30 y 14:30): ¿se siguió el plan A o se activó el plan B?

## Fuera de alcance (explícito, no silencioso)

| Elemento | Motivo |
| --- | --- |
| Auth0 | No refuerza la tesis de "sesión ya autenticada del usuario"; costo de 40-60 min no rentable hoy |
| Despliegue en Google Cloud Run | No suma puntos de rúbrica en un evento de un día; queda documentado como plan futuro |
| Flujo 2 (lectura de tabla) y Flujo 3 (revisión previa al envío) | Se construyen solo si el Flujo 1 está cerrado y estable — prioridad estricta |
| Base de datos persistente | Estado en memoria por `session_id` alcanza para la demo y el video |
| Bundler / React / Vite / webpack en la extensión | Un paso de build es un punto de fallo adicional; JS plano evita 20 min de riesgo |
