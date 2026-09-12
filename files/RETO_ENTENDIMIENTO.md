# RETO_ENTENDIMIENTO.md

**Proyecto:** Ventana — el agente que trabaja dentro de la pestaña que ya tienes abierta
**Hackathon:** Agents, Everywhere — AI Tinkerers Lima (competencia global)
**Fecha de build:** 12 de septiembre de 2026 · ventana real 11:15 a.m. – 3:30 p.m. (4h15)
**Equipo:** 4 personas (A · extensión, B · agente, C · entorno y pruebas, D · entrega)

Generado en Fase 0 del Prompt Maestro, a partir del informe de proyecto ya aprobado por el equipo. No se reinterpreta el tema del reto ni la rúbrica: se documentan tal como están.

---

## 1. Problema en una frase

Los sistemas donde ocurre el trabajo administrativo real en LATAM (mesas de partes, intranets, portales de trámites del Estado, ERPs legados) no tienen API y nunca la tendrán, así que ningún agente puede automatizarlos "desde fuera".

## 2. Qué NO quiere el reto (antipatrones que castiga la rúbrica)

- Un chatbot genérico con el entorno como decoración (criterio B, Innovación → 1-2/5).
- Una demo simulada o con datos precargados en vez de un flujo real end-to-end (criterio A → 1-2/5).
- Un "wrapper" superficial que no usa nada propio del entorno elegido (criterio B).
- Ejecución técnica sin manejo de errores visible (criterio C).
- Un agente que actúa sin control humano en acciones irreversibles (criterio D exige "control razonable").

## 3. Entidades y fuentes de datos, con volúmenes

| Entidad | Fuente | Volumen esperado |
| --- | --- | --- |
| Página del portal legado (DOM) | `portal-demo/` (clon local de un portal real de trámites) | 200 KB–2 MB de HTML crudo → se reduce a un índice de máx. 150 elementos / ≤6 KB JSON |
| Correo/PDF con datos de la solicitud | Caso de demo ficticio preparado por C | 1 texto libre por demo, con 8–10 campos a mapear |
| Tabla de expedientes | `extract_table` sobre el DOM | Hasta 200 filas |
| Verificación externa | Exa (`verify_entity`) | 1 consulta por dato a validar (ej. existencia de una empresa) |

## 4. Relaciones explícitas vs. relaciones a descubrir

- **Explícitas:** el mapeo `ref → label → value` de cada elemento del formulario ya lo entrega `indexPage()`; el contrato `/agent/turn` ya define request/response.
- **A descubrir en vivo:** a qué campo del formulario corresponde cada dato del correo (lo decide el modelo turno a turno, no está hardcodeado); qué elementos requieren verificación externa vía Exa.

## 5. Contrato de salida: qué debe mostrar cada resultado

Cada turno del agente debe mostrar, como mínimo:
- Un `reply` en lenguaje claro.
- La lista de `actions` propuestas, cada una con `reason` visible (por qué se propone ese valor).
- Un `trace` de los pasos dados (para demostrar orquestación real, no un happy path maquillado).
- El estado (`awaiting_approval` / `done` / `error`) siempre explícito.

## 6. Rúbrica oficial desglosada (fuente: agents-everywhere-hackathon-2.md), ordenada por lo que este proyecto ataca primero

| Criterio | Peso relativo en la estrategia | Cómo lo ataca Ventana |
| --- | --- | --- |
| **A. Requisitos y funcionalidad** | Máxima prioridad — sin esto no hay proyecto | Flujo 1 (llenado asistido) corriendo end-to-end sobre el portal clonado |
| **B. Innovación y alineación con el tema** | Alta — es el argumento central del informe | "Cuando no hay API, el navegador es la API": la sesión autenticada y el estado de pantalla no existen fuera del navegador |
| **C. Ejecución técnica e integración** | Alta | Índice compacto del DOM, 4 herramientas tipadas, reintento visible ante `ref_not_found` |
| **D. Utilidad y experiencia agéntica** | Alta | Aprobación humana por acción; el agente nunca envía |

## 7. Restricciones (tiempo, equipo, tecnologías)

- Ventana real de build: 4h15 (11:15–15:30), con envío al portal antes de las 15:30.
- Equipo de 4, roles fijos por frente (no por quién sabe más): A extensión, B agente, C entorno/pruebas, D entrega.
- Stack: Python + FastAPI + OpenAI Agents SDK (recomendado) o Java + Spring Boot (alternativa si el equipo no domina Python).
- Sin bundler en la extensión (JS plano). Sin base de datos (estado en memoria por `session_id`). Sin deploy antes de las 14:30.
- Elegibilidad: proyecto net-new construido durante el evento; librerías/plantillas permitidas, el core se construye hoy.

## 8. "Trampas" o reglas de interpretación clave

- No se trabaja contra el sitio en vivo: se clona el portal, conservando su fealdad estructural (tablas anidadas, IDs crípticos) porque esa fealdad es la prueba de que el enfoque funciona sobre sistemas reales.
- El botón de envío nunca lo pulsa el agente — no es una limitación técnica, es el argumento de control que puntúa el criterio D.
- El indexado excluye siempre `input[type="password"]`: ninguna credencial sale de la pestaña.
- Un proyecto al 70% entregado puntúa; uno al 95% sin enviar vale cero — por eso hay congelamiento de código a las 14:30 y D trabaja en la entrega desde las 11:15.

## 9. Las 3 cosas donde se gana o se pierde el reto

1. **Que el flujo 1 (llenado asistido) corra de verdad, en vivo, sobre el portal clonado** — sin esto, el criterio A hunde todo lo demás.
2. **Que la frase "esto no funcionaría en un chat" quede demostrada, no solo dicha** — la sesión autenticada y el estado de pantalla son el argumento de Innovación.
3. **Que se envíe antes de las 15:30** — el riesgo de mayor probabilidad según el propio informe es "llegar a las 3:30 sin enviar".

*No se inventan datos no especificados en el informe original; cualquier vacío se marca explícitamente como "no especificado".*
