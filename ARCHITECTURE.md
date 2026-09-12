# ARCHITECTURE.md

## Diagrama de capas (Pipeline + Hexagonal)

```
┌─────────────────────────────────────────┐
│  Navegador (pestaña del portal legado)  │
│  ┌───────────────────────────────────┐  │
│  │  Content script                    │  │
│  │  - indexa el DOM y asigna refs     │  │
│  │  - ejecuta acciones sobre el DOM   │  │
│  └──────────────┬────────────────────┘  │
│                 │ chrome.runtime         │
│  ┌──────────────▼────────────────────┐  │
│  │  Service worker (puente)           │  │
│  └──────────────┬────────────────────┘  │
│  ┌──────────────▼────────────────────┐  │
│  │  Side panel (UI del copiloto)      │  │
│  │  - input, plan de acciones,        │  │
│  │    aprobaciones, log, switch ES/EN │  │
│  └──────────────┬────────────────────┘  │
└─────────────────┼───────────────────────┘
                  │ HTTPS/HTTP(localhost)
┌─────────────────▼───────────────────────┐
│  Backend (local :8000)                  │
│  ┌───────────────────────────────────┐  │
│  │  Agent loop (OpenAI Agents SDK)    │  │
│  │  herramientas (dominio puro):      │  │
│  │   read_page · fill_field           │  │
│  │   extract_table · verify_entity    │  │
│  └───────────────────────────────────┘  │
└──────────────────────┬──────────────────┘
                       │
                  Exa (verify_entity)
```

## Regla de dependencias hacia adentro

- El **dominio** (`agent.py`, `tools.py` en el backend) no importa nada de la extensión ni del transporte HTTP: recibe `page.elements` ya indexado y devuelve `actions` ya tipadas.
- El **content script** no razona: solo indexa y ejecuta. Cero lógica de negocio en el cliente — esto es lo que permite pivotar de extensión a Slack (Punto de decisión 1) sin reescribir el backend.
- El **contrato `/agent/turn`** es el puerto (Ports & Adapters): cualquier canal (extensión hoy, CopilotKit Channels/Slack si se pivota) es un adaptador distinto sobre el mismo puerto.

## Flujo de datos (Flujo 1 — llenado asistido)

1. El usuario abre el side panel → `INDEX_PAGE` → content script indexa el DOM (máx. 150 elementos, ≤6 KB).
2. El panel llama `POST /agent/turn` con `message` + `page.elements` + el `locale` activo.
3. El backend ejecuta el agent loop: `read_page` (ya recibido), opcionalmente `verify_entity` (Exa), y arma un plan de `actions` con `fill_field` propuestos, cada uno con `reason`.
4. El panel pinta el plan; el usuario aprueba fila por fila.
5. El panel dispara `EXECUTE_ACTIONS` → el content script escribe cada campo disparando `input`/`change` con `bubbles: true`.
6. El panel devuelve `action_results` en un segundo `POST /agent/turn`. Si algo falló (`ref_not_found`), el agente re-lee la página una vez y reintenta — visible en el `trace` del log.
7. El agente nunca pulsa el botón de envío final: esa acción no existe como herramienta.

## Estructura de carpetas del repositorio

```
ventana/
├── extension/
│   ├── manifest.json
│   ├── content.js        # indexado del DOM + ejecución de acciones
│   ├── background.js     # puente entre panel y content script
│   ├── panel.html
│   ├── panel.js          # UI, aprobaciones, log
│   └── i18n/
│       ├── en.json       # claves de interfaz (inglés)
│       ├── es.json       # mismas claves exactas (español)
│       └── index.js      # t(key, params), detección y persistencia de locale
├── backend/
│   ├── main.py           # FastAPI, endpoint /agent/turn
│   ├── agent.py          # definición del agente y prompt de sistema
│   ├── tools.py          # las cuatro herramientas
│   └── requirements.txt
├── portal-demo/          # clon del portal + datos de prueba
├── docs/                 # RETO_ENTENDIMIENTO, ESTRATEGIA_SOLUCION, API_CONTRACTS
├── .sprints/              # BACKLOG.md + SPEC.md por sprint
└── README.md
```

**Decisiones de arquitectura tomadas y su justificación:**

- **Sin bundler en la extensión.** JS plano; un paso de build es un punto de fallo adicional.
- **Estado del backend en memoria**, un diccionario por `session_id`. Sin base de datos: el historial vive mientras el proceso corra, y eso alcanza para la demo y el video.
- **Capa i18n en el cliente, idioma en el contrato.** Los textos de interfaz se resuelven en la extensión vía `t()`; el idioma de lo que genera el modelo (`reply`, `reason`) viaja como `locale` en cada petición, porque no se puede resolver con un diccionario. Ver `docs/I18N_POLICY.md`.
- **Sin deploy hoy.** Backend en `localhost:8000`; la extensión declara `"host_permissions": ["http://localhost:8000/*"]`. Cloud Run queda documentado como plan futuro, no como tarea del día.
