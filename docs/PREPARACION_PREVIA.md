# PREPARACION_PREVIA.md

**Ventana: 10:00–11:00.** Todo esto se instala y se verifica mientras se llena la encuesta de créditos. Si alguien está instalando Python a las 11:30, el Sprint-01 ya se perdió.

## 10:00 — Lo primero, apenas lleguen

**Los cuatro llenan la encuesta de créditos.** OpenAI entrega un código único por asistente presencial elegible, sujeto a inventario; si el suministro se agota, el lugar se guarda **en el orden de finalización de la encuesta**. Llegar tarde a la encuesta es literalmente perder la cola.

## Checklist por persona

| Quién | Qué debe estar funcionando antes de las 11:15 | Verificado |
| --- | --- | --- |
| **Los cuatro** | Chrome actualizado · Git configurado · acceso al repo · encuesta de créditos completada · código de OpenAI en mano | [ ] |
| **A** (extensión) | Modo desarrollador activado en `chrome://extensions` y **una extensión de prueba cargada**, para confirmar que el flujo de carga funciona en su máquina | [ ] |
| **B** (agente) | Python 3.11+ · entorno virtual · `fastapi uvicorn openai-agents` instalados · **una llamada real a la API verificada**. Una clave que no sirve descubierta a las 12:00 es una hora perdida | [ ] |
| **C** (entorno) | Servidor estático corriendo (`python -m http.server 5500`) y `Save page as → Complete` **probado sobre un portal real** | [ ] |
| **D** (entrega) | Repo público de GitHub ya creado · grabador de pantalla probado **con audio** — que grabe 10 segundos y los reproduzca | [ ] |

## Comandos de verificación rápida

```bash
# B — entorno del backend
python --version                 # debe decir 3.11 o superior
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn openai-agents
python -c "import openai; print('SDK ok')"
# y una llamada real de prueba al modelo — no asumir que la clave sirve

# C — portal clonado
cd portal-demo && python -m http.server 5500
# abrir http://localhost:5500 y confirmar que el formulario carga
```

## 11:00–11:15 — Congelar antes de tocar código

En estos 15 minutos, con el equipo completo y en voz alta:

1. **Congelar la idea.** Entorno: navegador sobre portal legado. No se discute más.
2. **Congelar el stack.** Python + FastAPI + OpenAI Agents SDK (o Java solo si nadie está cómodo en Python). Decisión tomada a las 11:00, no después.
3. **Congelar el contrato** `docs/API_CONTRACTS.md`. Es lo único que A y B necesitan acordar. Con él fijo, trabajan en paralelo con mocks toda la tarde sin bloquearse.

Si a las 11:15 el contrato no está congelado, van a pasar la tarde sincronizándose en vez de construyendo.

## Requerimientos funcionales del MVP (orden estricto de prioridad)

Si no llegan a los dos últimos, no pasa nada. Si no llegan al primero, no hay proyecto.

1. El panel abre sobre la pestaña activa y muestra el índice de elementos detectados.
2. El agente recibe texto libre y devuelve un plan de llenado campo por campo con su justificación.
3. El usuario aprueba y los campos se llenan disparando `input` y `change`.
4. Ante `ref_not_found`, el agente re-lee la página una vez y reintenta, visible en el log.
5. El agente nunca pulsa enviar.
