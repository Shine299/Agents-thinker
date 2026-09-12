# SPEC-04: Congelamiento, pulido de entrega y envío (14:30–15:30)

Criterio de rúbrica objetivo: **Entrega** (sin esto, todo lo anterior vale cero — "un proyecto al 70% entregado puntúa; uno al 95% sin enviar vale cero")
Pre-existente o construido hoy: N/A — este sprint es documentación y empaquetado, no código nuevo.

Requisito previo: Punto de Decisión 2 (14:30) certificado por el Supervisor TDD, con toda fila en Rojo convertida en limitación conocida documentada.

## Escenario 1 — Code freeze real

Given: son las 14:30
When: cualquier frente (A, B, C) encuentra un bug
Then: NO se escribe código nuevo; el bug se anota en el README bajo "Limitaciones conocidas"

## Escenario 2 — Video final

Given: el guion de 2 minutos (problema → tesis → demo del flujo 1 → manejo de fallo → arquitectura → cierre)
When: se graba con el entorno real (portal clonado, panel, aprobación visible)
Then: el video muestra el cambio de idioma en vivo y dice literalmente la frase "Esto no funcionaría en un chat. El agente necesita estar dentro de la sesión del usuario, sobre la página que está viendo ahora mismo", y dura ≤2 minutos

## Escenario 3 — Envío completo

Given: los 5 elementos requeridos (título, descripción, repo público, video, post social)
When: D los sube al portal del hackathon
Then: el envío se confirma antes de las 15:30

## Criterios de aceptación (DoD) — checklist de entrega

- [ ] Título del proyecto
- [ ] Descripción escrita (problema, entorno, qué hace el agente, qué se construyó hoy)
- [ ] Repositorio público de GitHub con README que explique arquitectura y limitaciones conocidas
- [ ] Video de demostración de 2 minutos
- [ ] Post en redes sociales etiquetando a los partners del evento
- [ ] Enviado en el portal del hackathon antes de las 3:30 p.m.
- [ ] El README está íntegramente en inglés, incluidas las limitaciones conocidas
- [ ] El video muestra el cambio de idioma en vivo (ES → EN) durante la demo
- [ ] La explicación de elegibilidad (qué es pre-existente vs. construido hoy) está en el README, copiada de MEMORY.md

--- Bitácora del ciclo (llenar en vivo, con hora) ---
Verde certificado por Supervisor TDD (ENVÍO CONFIRMADO): [ ] Sí [ ] No — hora:
Veredicto final: ENVIADO / NO ENVIADO — si "NO ENVIADO", motivo:
