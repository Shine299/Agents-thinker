# SPEC-03: Integración real end-to-end + manejo de errores (13:30–14:30)

Criterio de rúbrica objetivo: **A** (funcionalidad end-to-end real) y **C** (manejo de fallos)
Pre-existente o construido hoy: todo se construye/integra hoy — esta es la fase donde desaparecen los mocks del Sprint-01.

## Escenario 1 — Fin de los mocks

Given: la extensión (frente A) y el backend (frente B) ya certificaron Verde por separado contra el contrato
When: el panel llama al backend real (no al mock) con un evento real del portal clonado
Then: la respuesta real se pinta en el panel, con el mismo formato que el mock — sin cambios de contrato de último minuto

## Escenario 2 — Mensajes de error legibles

Given: ocurre un `model_error` o un `ref_not_found` sin recuperación posible
When: el backend responde `status: "error"`
Then: el panel muestra un mensaje en español claro, no un stack trace ni un código crudo

## Escenario 3 — Prueba end-to-end en bucle

Given: el flujo 1 completo (pegar correo → plan → aprobar → llenado → confirmación)
When: se ejecuta 3 veces seguidas sin reiniciar el navegador
Then: las 3 corridas completan sin intervención manual fuera del panel (frente C prueba esto sin parar durante todo el sprint)

## Escenario 4 — Paridad de diccionarios (test automatizado)

Given: los archivos `en.json` y `es.json`
When: corre la suite de tests
Then: el test falla si existe una clave en un archivo y no en el otro. Es un fallo de test, no una advertencia

## Escenario 5 — End-to-end bilingüe

Given: el Flujo 1 completo
When: se ejecuta una corrida en `locale: "es"` y otra en `locale: "en"`
Then: ambas completan sin intervención manual, y ninguna respuesta mezcla idiomas

## Criterios de aceptación (DoD)

- [ ] Cero llamadas a datos mockeados quedan en el código de producción
- [ ] El primer corte del video (frente D) muestra al menos una corrida real, aunque no sea la final

--- Bitácora del ciclo (llenar en vivo, con hora) ---
Rojo certificado por Supervisor TDD:   [ ] Sí [ ] No — hora: — motivo:
Verde certificado por Supervisor TDD:  [ ] Sí [ ] No — hora: — motivo:
Dominio puro verificado:               [ ] Sí [ ] No
Contrato con el entorno respetado:     [ ] Sí [ ] No
Corrió con evento/dato real del entorno: [ ] Sí [ ] No
Veredicto final: APROBADO / RECHAZADO

---

## Auditoría de Punto de Decisión 2 (14:30 — congelamiento absoluto)

| # | Pregunta | Verde/Ámbar/Rojo | Acción si no es Verde |
| --- | --- | --- | --- |
| 1 | ¿El flujo 1 corre end-to-end sobre el portal clonado, con una entrada nueva, ahora mismo? | | |
| 2 | ¿El entorno (navegador + sesión) sigue siendo protagonista o se volvió wrapper por falta de tiempo? | | |
| 3 | ¿Las llamadas a Exa/OpenAI son reales o quedó algo simulado? | | |
| 4 | ¿Un usuario entendería el valor del panel sin explicación extra? | | |
| 5 | ¿El plan B (OpenRouter si se agota el crédito) está probado o solo documentado? | | |
| 6 | ¿README, guion de video y post social están en progreso real (frente D)? | | |
| 7 | ¿El README público está íntegramente en inglés, sin español residual? | | |
| 8 | ¿Quedó algún string visible hardcodeado, o alguna clave desalineada entre `en.json` y `es.json`? | | |

**Regla dura de esta auditoría:** cualquier fila en Rojo a las 14:30 se declara como limitación conocida en el README — no se abre tarea nueva para arreglarla.
