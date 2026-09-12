# AGENTS.md

Reglas de operación para trabajar híbridamente (humanos + agentes de código) sobre el proyecto **Ventana**, en 4 sprints dentro de la ventana real 11:15–15:30.

## Roles con autoridad separada

**ROL 1 — Development Team** (uno por frente: A extensión, B agente, C entorno/pruebas, D entrega). Construye bajo SDD + Arquitectura Limpia/Hexagonal + Scrum de 4 sprints.

**ROL 2 — Supervisor TDD** (control de calidad y de reloj, independiente de los 4 frentes). No escribe features. Certifica el ciclo Rojo→Verde de cada tarea y preside los 2 puntos de decisión del cronograma (12:30 y 14:30). Tiene veto: sin su aprobación no hay "Done" en BACKLOG.md ni avance de sprint.

## Reglas inquebrantables

1. Nada de código sin un SPEC.md que lo contrate.
2. TDD siempre: primero el test que falla (Rojo), luego el código mínimo (Verde). El Supervisor certifica cada transición con evidencia real (output de la corrida).
3. El contrato `docs/API_CONTRACTS.md` se congela a las 11:15. A y B trabajan contra mocks de ese contrato; no se renegocia durante el build.
4. Dominio puro en el backend: `tools.py`/`agent.py` no dependen de detalles de la extensión, y viceversa.
5. Toda dependencia externa (modelo, Exa) tiene degradación elegante: `model_error` se reporta legible, nunca rompe el panel. OpenRouter como ruta de respaldo si el crédito de OpenAI se agota.
6. Un solo reintento por acción ante `ref_not_found`, nunca en bucle, nunca fallar en silencio.
7. Ninguna acción con `needs_approval: true` se ejecuta sin clic del usuario. El agente nunca envía — la herramienta de envío no se implementa, ni siquiera deshabilitada.
8. El indexado excluye siempre `input[type="password"]`.
9. Cero funcionalidades fuera del alcance del SPEC activo del sprint en curso.
10. Todo el backlog cabe en 4 sprints dentro de 11:15–15:00 (freeze real 30 min antes del límite del portal, 15:30). No hay Sprint-05.
11. Cada tarea del backlog declara a qué criterio de la rúbrica oficial ataca (A: funcionalidad, B: innovación, C: ejecución técnica, D: utilidad agéntica). Si no ataca ninguno, no entra al backlog.
12. D trabaja en la entrega (README, guion, video, post, envío) desde las 11:15, no desde el final.
13. Punto de decisión 1 (12:30): si la extensión no carga y no se comunica con el backend, se pivota a CopilotKit Channels → Slack, reusando el mismo backend y las mismas herramientas, sin reescribir nada — por eso el canal va desacoplado desde el primer commit.
14. Punto de decisión 2 (14:30): congelamiento absoluto de código. Cualquier bug posterior se documenta como limitación conocida en el README, no se arregla.
15. **Idioma (ver `docs/I18N_POLICY.md`).** Todo el código, los identificadores, los comentarios, los mensajes de commit y el `README.md` público van **en inglés**. La interfaz del producto es **bilingüe ES/EN** seleccionable en runtime. Ningún string visible al usuario se escribe embebido en el código: sale de `extension/i18n/{en,es}.json`, que deben tener claves idénticas. El agente responde en el `locale` que recibe en la petición, sin mezclar idiomas.
16. Registrar en MEMORY.md, desde la primera línea, qué parte es pre-existente (librería/plantilla permitida) y qué parte se construyó durante el evento, para responder la pregunta de elegibilidad sin dudar.

## Comunicación

- Tablas de doble entrada, nunca prosa larga.
- El Supervisor declara explícitamente "Supervisor TDD: APROBADO" o "Supervisor TDD: RECHAZADO — motivo" en cada certificación.
- Al cerrar cualquier tarea, decisiones, atajos y errores van a MEMORY.md con la hora.

## Documentos de apoyo (consultar durante el build)

| Documento | Cuándo se usa |
| --- | --- |
| `docs/I18N_POLICY.md` | A y B, en cada tarea que toque texto o código |
| `docs/PREPARACION_PREVIA.md` | 10:00–11:15, antes de tocar código |
| `docs/RIESGOS.md` | Abierto todo el build; C y el Supervisor lo revisan en cada punto de decisión |
| `docs/GUION_VIDEO.md` | D, desde las 11:15; primer corte 13:30, final 15:00 |
| `docs/CREDITOS_SPONSORS.md` | 10:00 (encuesta) y 14:00 (decisión sobre Ambiguous AI) |
| `docs/PENDIENTES.md` | Quien canjee las claves de OpenAI/Exa, apenas las tenga — activa el modo real sin tocar código |
| `README.md` | D, desde las 11:15; limitaciones conocidas se llenan a las 14:30 |

**Estado de estas reglas: Activa.**
