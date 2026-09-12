# GUION_VIDEO.md

**El video es lo que puntúa el jurado global, no el show-and-tell local.** Se guioniza y se graba con calma, sin improvisar. Duración máxima: 2 minutos. Dueño: D. Primer corte a las 13:30, final a las 15:00.

## Estructura por tiempos

| Tiempo | Contenido | Qué debe verse en pantalla | Criterio que gana |
| --- | --- | --- | --- |
| 0:00–0:15 | El problema en una frase: sistemas donde no hay API y nunca la habrá | El portal real en pantalla, con su fealdad estructural visible | Contexto |
| 0:15–0:30 | La tesis: cuando no hay API, el navegador es la API. El agente entra por donde entra el usuario | El side panel abriéndose sobre la pestaña ya autenticada | **B — Innovación** |
| 0:30–1:15 | **Demo del Flujo 1.** Pegar el correo → el agente lee la página → propone el llenado campo por campo → el usuario aprueba → los campos se llenan solos | El panel con el plan de acciones visible, cada fila con su `reason` | **A — Funcionalidad** |
| 1:15–1:35 | Manejo de fallo: un elemento no encontrado, el agente re-lee la página y se recupera. Y el botón de enviar lo pulsa la persona, no el agente | El `trace` en el log del panel mostrando el reintento. El cursor humano sobre el botón de envío | **C — Ejecución** y **D — Control** |
| 1:35–1:45 | **Cambio de idioma en vivo**: pulsar EN en la cabecera y mostrar que el panel y la siguiente respuesta del agente cambian de idioma sin perder la sesión | El selector ES/EN y el historial intacto | **D — Utilidad** |
| 1:45–1:50 | La arquitectura en una imagen: índice compacto del DOM, cuatro herramientas, aprobación humana | Diagrama estático de `ARCHITECTURE.md` | **C — Ejecución** |
| 1:50–2:00 | Qué se construyó hoy y qué sigue. Agradecer y etiquetar a los partners | Pantalla de cierre con logos/handles | Elegibilidad |

## Frases que conviene decir literalmente

**La frase que entrega el criterio de Innovación ya masticado al jurado:**

> "Esto no funcionaría en un chat. El agente necesita estar dentro de la sesión del usuario, sobre la página que está viendo ahora mismo."

**La frase que separa un 4 de un 5 en ejecución técnica** (decirla mientras se muestra el índice):

> "El indexado excluye todo campo de contraseña. Ninguna credencial sale de la pestaña."

**La frase bilingüe** (decirla en el cambio de idioma, 1:35–1:45):

> "The portals are in Spanish. The people using them work in Spanish. The agent speaks their language — and it speaks yours."

**La frase de control de usuario** (decirla en el minuto 1:15–1:35):

> "El agente puede leer, puede proponer, puede escribir tras aprobación. Lo que nunca hace es enviar. Esa herramienta no está deshabilitada: no existe."

## Reglas de grabación

- Grabar con audio. Probar el grabador **con audio** antes de las 11:15 (ver `PREPARACION_PREVIA.md`).
- Tener un primer corte a las 13:30 con lo que haya. Un video parcial es respaldo; no tener nada a las 15:00 es cero.
- Mostrar una corrida real sobre el portal clonado, no capturas ni resultados precargados.
- No exceder los 2 minutos. Si sobra contenido, se recorta la sección de arquitectura (1:35–1:50), nunca la demo.

## Checklist antes de exportar

- [ ] Dura 2 minutos o menos
- [ ] Se ve una corrida end-to-end real del Flujo 1, con entrada nueva
- [ ] Se ve el reintento tras `ref_not_found` en el log
- [ ] Se ve que el humano pulsa el botón de envío, no el agente
- [ ] Se dijo la frase de Innovación literalmente
- [ ] Se mostró el cambio de idioma ES → EN en vivo, sin perder la sesión
- [ ] Se mencionó qué se construyó hoy (elegibilidad)
- [ ] Se etiquetó a los partners
