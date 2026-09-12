# SPEC-02: Llenado real, aprobación, Exa (12:30–13:30)

Criterio de rúbrica objetivo: **C** (ejecución técnica) y **D** (control del usuario)
Pre-existente o construido hoy: Exa API es servicio de sponsor (pre-existente); la herramienta `verify_entity`, el flujo de aprobación y el reintento se escriben hoy.

Requisito previo: Punto de Decisión 1 (12:30) cerrado en Verde o Ámbar por el Supervisor TDD. Si fue Rojo, este SPEC no se abre hasta activar el plan B (Slack) y re-certificar.

## Escenario 1 — Llenado dispara validadores reales

Given: un campo de texto vacío en el formulario clonado, con `ref = e12`
When: el agente ejecuta `fill_field` con `{ ref: "e12", value: "Juan Pérez Quispe" }`
Then: el campo muestra el valor Y el portal lo reconoce como válido (los eventos `input`/`change` con `bubbles: true` se dispararon)

## Escenario 2 — Ninguna acción sin aprobación

Given: el agente propuso 8 acciones de `fill_field`
When: el usuario aprueba solo 5 de ellas
Then: únicamente esas 5 se ejecutan sobre el DOM; las otras 3 quedan pendientes

## Escenario 3 — Reintento único ante `ref_not_found`

Given: una acción de `fill_field` referencia un `ref` que ya no existe en el DOM
When: se ejecuta la acción
Then: el agente re-ejecuta `read_page` una vez, reintenta con el índice nuevo, y si vuelve a fallar se detiene y lo reporta en el panel — visible en el `trace`, nunca en bucle

## Escenario 4 — Verificación externa vía Exa

Given: el correo de demo menciona una empresa que debe validarse
When: el agente detecta ese dato como verificable
Then: llama `verify_entity` y el resultado de Exa aparece en el `trace` antes de proponer el campo correspondiente

## Escenario 5 — Cambio de idioma en caliente

Given: una sesión activa en español con 8 acciones ya propuestas
When: el usuario pulsa el selector EN en la cabecera
Then: los textos de interfaz cambian a inglés, la elección persiste en `chrome.storage.local`, el historial de la sesión NO se pierde, y las respuestas siguientes del agente llegan en inglés

## Escenario 6 — Errores traducidos, códigos técnicos ocultos

Given: una acción falla con `ref_not_found`
When: el panel muestra el fallo
Then: el usuario ve el texto de `error.refNotFound` en su idioma activo; el código crudo `ref_not_found` aparece solo en el `trace`, nunca en el mensaje al usuario

## Criterios de aceptación (DoD)

- [ ] El caso de demo (correo ficticio, 8-10 campos, 1 dato verificable por Exa, 1 dato que requiere transformación) está listo
- [ ] Ninguna acción con `needs_approval: true` se ejecuta sin clic del usuario
- [ ] Los `label` del formulario y los `ref` se citan textualmente dentro de `reason`, sin traducirse
- [ ] Ningún string visible al usuario quedó hardcodeado en `extension/` ni en `backend/`

--- Bitácora del ciclo (llenar en vivo, con hora) ---
Rojo certificado por Supervisor TDD:   [ ] Sí [ ] No — hora: — motivo:
Verde certificado por Supervisor TDD:  [ ] Sí [ ] No — hora: — motivo:
Dominio puro verificado:               [ ] Sí [ ] No
Contrato con el entorno respetado:     [ ] Sí [ ] No
Corrió con evento/dato real del entorno: [ ] Sí [ ] No
Veredicto final: APROBADO / RECHAZADO
