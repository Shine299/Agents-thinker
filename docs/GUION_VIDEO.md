# GUION_VIDEO.md

**El video es lo que puntúa el jurado global, no el show-and-tell local.** Se guioniza y se graba con calma, sin improvisar. Duración máxima: 2 minutos. Dueño: D. Primer corte a las 13:30, final a las 15:00.

## Estructura por tiempos

| Tiempo | Contenido | Qué debe verse en pantalla | Criterio que gana |
| --- | --- | --- | --- |
| 0:00–0:15 | El problema en una frase: sistemas donde no hay API y nunca la habrá | El portal real en pantalla, con su fealdad estructural visible | Contexto |
| 0:15–0:30 | Se nombra el producto: Wicket AI. La tesis: cuando no hay API, el navegador es la API. El agente entra por donde entra el usuario | El side panel abriéndose sobre la pestaña ya autenticada | **B — Innovación** |
| 0:30–1:15 | **Demo del Flujo 1.** Pegar el correo → el agente lee la página → propone el llenado campo por campo → el usuario aprueba → los campos se llenan solos | El panel con el plan de acciones visible, cada fila con su `reason` | **A — Funcionalidad** |
| 1:15–1:35 | Manejo de fallo: un elemento no encontrado, el agente re-lee la página y se recupera. Y el botón de enviar lo pulsa la persona, no el agente | El `trace` en el log del panel mostrando el reintento. El cursor humano sobre el botón de envío | **C — Ejecución** y **D — Control** |
| 1:35–1:45 | **Cambio de idioma en vivo**: pulsar EN en la cabecera y mostrar que el panel y la siguiente respuesta del agente cambian de idioma sin perder la sesión | El selector ES/EN y el historial intacto | **D — Utilidad** |
| 1:45–1:50 | La arquitectura en una imagen: índice compacto del DOM, cuatro herramientas, aprobación humana | Diagrama estático de `ARCHITECTURE.md` | **C — Ejecución** |
| 1:50–2:00 | Qué se construyó hoy y qué sigue. Agradecer y etiquetar a los partners | Pantalla de cierre con logos/handles | Elegibilidad |

## Guion exacto (palabra por palabra, listo para leer al grabar)

Narración en español, con una frase en inglés a propósito en el cambio de idioma (0:35–0:45) — es la prueba en vivo de que el producto es bilingüe, no solo una traducción de UI. El nombre del producto es **Wicket AI**; decirlo completo la primera vez (0:15) y una vez más durante la demo (0:30–1:15), nunca "Ventana" (nombre interno de trabajo, no el nombre público).

**0:00–0:15** — mostrando `mesa-partes.html`, panel cerrado:
> "Todo agente de IA asume que el sistema tiene una API. Los sistemas donde se hace el trabajo administrativo en Latinoamérica no la tienen, y nunca la tendrán: mesas de partes, intranets universitarias, portales públicos, ERPs de hace quince años."

**0:15–0:30** — abriendo el side panel sobre la misma pestaña:
> "Wicket AI es el agente que trabaja dentro de la pestaña que ya tienes abierta. Esto no funcionaría en un chat. El agente necesita estar dentro de la sesión del usuario, sobre la página que está viendo ahora mismo."

**0:30–1:15** — pegar el correo, esperar la propuesta, señalar la fila del RUC:
> "Pego el correo de la solicitud. Wicket AI lee la página y propone el llenado campo por campo, cada uno con su razonamiento. Este RUC lo verificó contra una fuente externa antes de proponerlo — encontró una discrepancia, me lo dice aquí, y aun así la decisión de aprobarlo es mía."

**1:15–1:35** — F5 en el portal, aprobar, ver el reintento, aprobar el resto, pulsar tú "Enviar Solicitud":
> "Si la página cambia debajo del agente, se da cuenta, vuelve a leerla, y reintenta una sola vez — nunca en bucle, nunca en silencio. El agente puede leer, puede proponer, puede escribir tras aprobación. Lo que nunca hace es enviar. Esa herramienta no está deshabilitada: no existe."

**1:35–1:45** — cambiar ES→EN en la cabecera, mandar un mensaje corto:
> "The portals are in Spanish. The people using them work in Spanish. The agent speaks their language — and it speaks yours."

**1:45–1:50** — diagrama estático de `ARCHITECTURE.md`:
> "Por dentro: un índice compacto del DOM en vez del HTML completo, tres herramientas, y aprobación humana en cada paso que escribe algo. El indexado excluye todo campo de contraseña. Ninguna credencial sale de la pestaña."

**1:50–2:00** — pantalla de cierre con logos:
> "Todo esto se construyó hoy, en las horas del evento. Gracias a AI Tinkerers Lima, a OpenAI y a Exa."

## Las 4 frases clave (referencia rápida en cámara — texto completo en "Guion exacto" arriba)

| Cuándo | Frase | Por qué |
| --- | --- | --- |
| 0:15–0:30 | "Esto no funcionaría en un chat. El agente necesita estar dentro de la sesión del usuario, sobre la página que está viendo ahora mismo." | Criterio B — Innovación |
| 1:45–1:50 | "El indexado excluye todo campo de contraseña. Ninguna credencial sale de la pestaña." | Criterio C — Ejecución técnica |
| 1:35–1:45 | "The portals are in Spanish. The people using them work in Spanish. The agent speaks their language — and it speaks yours." | Criterio D — Utilidad, en inglés a propósito |
| 1:15–1:35 | "El agente puede leer, puede proponer, puede escribir tras aprobación. Lo que nunca hace es enviar. Esa herramienta no está deshabilitada: no existe." | Criterio D — Control del usuario |

## Reglas de grabación

- Grabar con audio. Probar el grabador **con audio** antes de las 11:15 (ver `PREPARACION_PREVIA.md`).
- Tener un primer corte a las 13:30 con lo que haya. Un video parcial es respaldo; no tener nada a las 15:00 es cero.
- Mostrar una corrida real sobre el portal clonado, no capturas ni resultados precargados.
- No exceder los 2 minutos. Si sobra contenido, se recorta la sección de arquitectura (1:35–1:50), nunca la demo.

## Corrida guionizada para grabar (Sprint-03, con claves reales)

Entorno: backend en `:8000` (claves reales activas), portal en `:5500/mesa-partes.html`, extensión cargada.

| Tiempo del guion | Acción exacta | Qué se dice |
| --- | --- | --- |
| 0:00–0:15 | Mostrar `mesa-partes.html` cargado, sin el panel abierto | Párrafo 1 del "Guion exacto" |
| 0:15–0:30 | Abrir el side panel sobre la misma pestaña | Párrafo 2 — aquí se nombra "Wicket AI" por primera vez y va la frase de Innovación |
| 0:30–1:15 | Pegar el correo de `portal-demo/demo-case.txt` (solo el cuerpo del correo, sin las notas internas). Enviar. Esperar la respuesta (6–11s reales). Señalar la fila del RUC en el plan de acciones | Párrafo 3 — segunda vez que se nombra "Wicket AI"; la discrepancia del RUC (verificación real de Exa) sale en el `reason` de esa fila |
| 1:15–1:35 | Antes de aprobar el primer campo, pulsar F5 en la pestaña del portal (se pierden los `data-ventana-ref`, id técnico interno — no se menciona en voz). Aprobar ese campo → aparece `ref_not_found` → el log muestra el paso `retry` → nueva propuesta con ref fresco → aprobar de nuevo, el campo se llena y se pone verde. Aprobar el resto y pulsar tú el botón "Enviar Solicitud" | Párrafo 4 — frase de control de usuario |
| 1:35–1:45 | Cambiar ES→EN en la cabecera a mitad de sesión, mandar un mensaje corto nuevo | Párrafo 5 — la frase bilingüe, en inglés, literal |
| 1:45–1:50 | Diagrama estático de `ARCHITECTURE.md` | Párrafo 6 |
| 1:50–2:00 | Cierre, elegibilidad, logos de partners | Párrafo 7 |

**Momento vendible nuevo (verificado hoy con Exa real):** el `reason` del campo RUC mostrando la discrepancia es la prueba en vivo de que el agente verifica contra una fuente externa y nunca decide por el humano — enlaza directo con la frase de control de usuario.

## Checklist antes de exportar

- [ ] Dura 2 minutos o menos
- [ ] Se dijo "Wicket AI" completo al menos dos veces (0:15 y 0:30–1:15), nunca "Ventana"
- [ ] Se ve una corrida end-to-end real del Flujo 1, con entrada nueva
- [ ] Se ve el reintento tras `ref_not_found` en el log
- [ ] Se ve la verificación externa (Exa) en el `reason` de un campo, con su posible discrepancia
- [ ] Se ve que el humano pulsa el botón de envío, no el agente
- [ ] Se dijo la frase de Innovación literalmente
- [ ] Se mostró el cambio de idioma ES → EN en vivo, sin perder la sesión
- [ ] Se mencionó qué se construyó hoy (elegibilidad)
- [ ] Se etiquetó a los partners
