# ESTRATEGIA_SOLUCION.md

Generado en Fase 0 del Prompt Maestro. El equipo ya decidió; este documento dejó registro de las 3 alternativas evaluadas y por qué se eligió la que está en el informe.

---

## Propuesta 1 (segura) — Formulario web propio con agente de llenado

- **Idea central:** construir un formulario web propio (no un portal legado real) y un agente que lo llena a partir de texto libre.
- **Stack:** cualquier framework web + LLM directo.
- **Ataque a la rúbrica:** cumple A fácilmente, pero **B (Innovación) cae a 2/5**: es un entorno controlado por el propio equipo, no "un lugar donde la gente ya trabaja". El jurado lo lee como demo de laboratorio.
- **Riesgo:** bajo técnicamente, alto en alineación al tema.
- **Trampas:** cae directo en "chatbot genérico con entorno irrelevante".

## Propuesta 2 (ambiciosa) — Agente que opera sobre un portal gubernamental en vivo

- **Idea central:** automatizar directamente un portal de trámites real, en producción.
- **Stack:** extensión + backend, igual que Propuesta 3, pero contra el sitio real.
- **Ataque a la rúbrica:** el más fuerte posible en B si funciona, pero **A y C en riesgo crítico**: el sitio puede caerse o cambiar a mitad de demo, y muchos portales estatales prohíben automatización en sus términos.
- **Riesgo:** alto — depende de un sistema que el equipo no controla, en una ventana de 4h15.
- **Trampas:** "demo dependiente de un tercero fuera de control" — el Kit LEAD UTP es explícito: siempre plan B local.

## Propuesta 3 (elegida) — Extensión de navegador (side panel) sobre un clon local del portal

- **Idea central:** *Ventana* — copiloto de navegador que ve la página activa (un clon local de un portal legado real) y actúa sobre ella con aprobación humana en cada acción que modifica algo.
- **Stack:** extensión JS plana (manifest MV3, content script, side panel) + backend Python/FastAPI + OpenAI Agents SDK + Exa para verificación externa.
- **Ataque a la rúbrica:**
  - **A:** flujo de llenado completo end-to-end sobre un entorno estable (el clon local no se cae ni cambia).
  - **B:** máximo — el valor central (sesión autenticada + estado real de pantalla) es irreproducible en un chatbox aislado.
  - **C:** índice compacto del DOM, 4 herramientas tipadas, reintento visible ante fallos.
  - **D:** aprobación humana obligatoria por acción; el agente nunca envía.
- **Riesgo:** controlado — el clon local elimina el riesgo del sitio cayéndose, y el contrato `/agent/turn` desacopla extensión y backend desde el minuto 1, permitiendo trabajo en paralelo.
- **Combina lo mejor de las otras dos:** tiene la ambición temática de la Propuesta 2 (portal real, no un juguete) sin heredar su riesgo de infraestructura fuera de control, y tiene la estabilidad técnica de la Propuesta 1 sin su debilidad en Innovación.

## Recomendación final

**Propuesta 3.** Es la única que responde de frente a las 3 preguntas de la compuerta del Prompt Maestro: el entorno (navegador sobre sesión autenticada) es protagonista, no decoración; el agente hace algo que un chat no podría (leer/escribir sobre el DOM real de una sesión ya iniciada); y el riesgo de tiempo está controlado por el clon local y el contrato congelado a las 11:15.

**Decisión de stack tomada:** Python + FastAPI + OpenAI Agents SDK (ahorra 45–60 min de agent loop propio frente a Java + Spring Boot). Alternativa Java solo si nadie del equipo está cómodo en Python.

**Decisión de despliegue tomada:** nada se despliega hoy. Backend en `localhost:8000`, sin Docker ni Cloud Run antes del congelamiento de código (14:30). Cloud Run queda documentado como plan futuro en el README, no como tarea del día.

**Sponsors descartados conscientemente:** Auth0 (no refuerza la tesis de "sesión ya autenticada del usuario" y cuesta 40-60 min); Cloud Run (no suma puntos de rúbrica en un evento de un día). Ambiguous AI queda como tarea opcional de D solo si sobra tiempo a las 14:00.
