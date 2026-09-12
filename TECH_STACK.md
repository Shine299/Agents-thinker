# TECH_STACK.md

## Permitidas (y por qué)

| Tecnología | Para qué | Justificación contra la rúbrica |
| --- | --- | --- |
| **Python 3.11+ / FastAPI** | Backend, endpoint `/agent/turn` | Rápido de levantar sin build step; deja tiempo para C (criterio A: MVP end-to-end) |
| **OpenAI Agents SDK** | Agent loop, tool calling | Regala el loop y el manejo de herramientas — ahorra 45-60 min frente a escribirlo a mano (crítico en 4h15). Justifica el criterio C (ejecución técnica) sin gastar el tiempo en infraestructura propia |
| **JavaScript plano (sin bundler)** | Extensión MV3: content script, side panel | Un paso de build (React/Vite/webpack) es un punto de fallo que no se recupera en una ventana de 4h15 |
| **Exa** | Herramienta `verify_entity` | Validación de datos externos real (empresa, dirección), demostrable en el video — sponsor con oferta compartida ya desbloqueada en la encuesta de créditos |
| **OpenRouter** | Ruta de respaldo | Si el crédito de OpenAI se agota a media tarde, mismo formato de llamada, cero refactor |
| **ngrok / Cloudflare Tunnel** | Solo si se necesita URL pública para grabar desde otra máquina | 2 minutos de setup, sin salir de la laptop; no se usa si no hace falta |

## Vetadas hoy (y por qué)

| Tecnología | Motivo |
| --- | --- |
| **Docker / Google Cloud Run** | No suma puntos de rúbrica en un evento de un día — el jurado puntúa el video y el repo, no la URL desplegada. Recuperar 30-40 min es el 15% del tiempo total. Queda documentado en el README como plan futuro |
| **Auth0** | El plan Free cubriría el evento sin costo, pero montar autenticación propia no refuerza la tesis del proyecto ("el agente opera dentro de la sesión que el usuario ya tiene abierta") y cuesta 40-60 min que rinden más en `labelFor` y manejo de errores |
| **React / Vite / webpack (extensión)** | Un paso de build adicional es superficie de fallo innecesaria en 4h15 |
| **Base de datos persistente** | El estado en memoria por `session_id` alcanza para demo + video; una BD real consume tiempo de scaffolding sin subir ningún criterio de la rúbrica hoy |
| **Java + Spring Boot** | Terreno conocido, pero el agent loop y el tool calling se escriben a mano — se usa solo como alternativa si nadie del equipo está cómodo en Python |

## Norma de idioma (vinculante)

Sin librería de i18n. Un `t(key, params)` propio de ~20 líneas sobre dos JSON planos es suficiente para 6 módulos de interfaz y evita añadir una dependencia y su configuración en una ventana de 4h15. Código, identificadores, comentarios, commits y README **en inglés**; interfaz **bilingüe ES/EN**. Detalle completo en `docs/I18N_POLICY.md`.

## Decisión de despliegue

Nada se despliega hoy. Backend en `localhost:8000`; la extensión declara el permiso de host correspondiente. Respaldo si se necesita URL pública: túnel (ngrok/Cloudflare), no despliegue completo.

## No hay `database/schema.sql` en este proyecto

El backend mantiene el estado de la sesión en memoria (`dict` por `session_id`), sin persistencia. Se documenta aquí en vez de generar un schema.sql vacío o artificial — esto es una decisión de arquitectura, no un archivo pendiente.
