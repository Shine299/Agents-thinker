# CREDITOS_SPONSORS.md

## Advertencia primero

**La encuesta de créditos solo desbloquea tres cosas: OpenAI, OpenRouter y Exa.** Cloud Run, Auth0, CopilotKit, Trigger.dev, Ambiguous AI y Mozilla.ai aparecen como sponsors con guías técnicas, **no con códigos en ese paquete**. Cada uno se gestiona desde su propia página de hackathon. En el caso de Cloud Run y Auth0, sus capas gratuitas ya cubrirían todo lo que este proyecto necesitaría — no hace falta código de canje.

Los códigos son **privados e intransferibles**, y no hay soporte para errores de canje. Lean las instrucciones antes de pegar nada.

## Qué canjear y para qué en este proyecto

| Sponsor | Para qué en Ventana | Prioridad | Cómo se obtiene |
| --- | --- | --- | --- |
| **OpenAI** | Motor del agent loop y del tool calling | **Crítica** | Código único por asistente presencial elegible, sujeto a inventario. El orden de finalización de la encuesta define la cola → llenarla a las 10:00 |
| **Exa** | Herramienta `verify_entity` para validación de datos externos | **Alta** | Oferta compartida vía encuesta |
| **OpenRouter** | Ruta de respaldo si el crédito de OpenAI se agota (mismo formato de llamada, cero refactor) | **Respaldo** | Enlace por ciudad registrada vía encuesta |
| **Ambiguous AI** | Solo si D queda libre a las 14:00: destino del registro de acciones del agente | **Opcional** | Página propia de hackathon, no la encuesta |
| **Google Cloud Run** | No se usa hoy. Capa gratuita permanente (2M peticiones, 180.000 vCPU-s, 360.000 GiB-s al mes). Queda como plan de despliegue documentado en el README | **Descartada del día** | No requiere canje |
| **Auth0** | Fuera de alcance. Plan Free hasta 25.000 usuarios activos mensuales, pero no refuerza la tesis del proyecto y cuesta ~1 hora | **Descartada** | No requiere canje |
| **CopilotKit** | Solo si se activa el plan B del Punto de Decisión 1: Channels → Slack | **Contingente** | Página propia de hackathon |

## Por qué se descartó Auth0, explícitamente

El argumento central del proyecto es que **el agente opera dentro de la sesión que el usuario ya tiene abierta** en el portal. Montar una capa de autenticación propia no refuerza esa tesis ante el jurado, y cuesta entre 40 y 60 minutos que rinden mucho más invertidos en `labelFor` y en el manejo de errores. Si el equipo quiere presencia de sponsor visible, **Exa la da más barata y más demostrable**.

## La oportunidad de menor competencia

Si D termina sus tareas de entrega a las 14:00, conectar **Ambiguous AI** como destino del registro de lo que el agente hizo en el portal cuesta ~45 minutos, no toca el proyecto principal, y abre la elegibilidad al premio dedicado (**NVIDIA DGX Spark**), que es el de menor competencia del evento.

Condición dura: esto solo se hace si el Punto de Decisión 2 (14:30) no tiene filas en Rojo y si la entrega principal ya está asegurada. Nunca antes.
