# PENDIENTES.md

**Estado (2026-09-12): las claves de OpenAI y Exa ya están activas y verificadas.** Sprint-01 y Sprint-02 cerrados (ver `MEMORY.md`). Este archivo queda como guía operativa para quien tenga que reponer una clave o cambiar el modelo.

---

## Configuración (backend/.env)

```bash
cd backend
cp .env.example .env    # solo si aún no existe
```

| Variable | Obligatoria | Efecto |
| --- | --- | --- |
| `OPENAI_API_KEY` | Sí | Modelo del agente. Sin crédito responde `model_error: RateLimitError` (el panel lo muestra legible, no rompe) |
| `EXA_API_KEY` | Sí | `verify_entity`. Sin ella, la tool corre en stub determinista |
| `OPENROUTER_API_KEY` | No | Respaldo si se agota el crédito de OpenAI. Solo se usa si `OPENAI_API_KEY` está vacía |
| `VENTANA_MODEL` | No | Modelo (default `gpt-4o-mini`). No usar modelos razonadores: tardan >10s y el timeout es 20s |
| `VENTANA_AGENT_BACKEND` | **Déjala comentada** | Si vale `stub`, ignora todas las claves. Nunca para la demo ni el video |

`main.py` carga el `.env` solo; basta reiniciar:

```bash
.venv/bin/uvicorn main:app --port 8000
```

## Verificar que corre en modo real (1 minuto)

```bash
cd backend && .venv/bin/python -m pytest tests/ -q      # 46 passed
cd extension && node run-benches.mjs                    # 20 PASS + 15 PASS (npm install --no-save jsdom, una vez)
```

Y contra el backend corriendo:

```bash
curl -s -X POST localhost:8000/agent/turn -H 'Content-Type: application/json' -d '{
  "session_id": "s_check", "locale": "es",
  "message": "Solicitud de GRUPO ANDINO SAC con RUC 20456789123.",
  "page": {"url":"http://x","title":"t","elements":[
    {"ref":"e0","tag":"input","type":"text","label":"Razon social de la empresa","value":"","options":null,"required":false}
  ]}, "action_results": null}' | python3 -m json.tool
```

En `trace`:
- `"provider=openai"` + `"exa: found — ..."` → **modo real**.
- `"stub: match for '...'"` → sigue en stub: revisa `VENTANA_AGENT_BACKEND` en `.env`.
- `"model_error: RateLimitError"` → la cuenta de OpenAI no tiene crédito.
- `"timeout after 20s"` → modelo lento; revisa `VENTANA_MODEL`.

## Qué NO hacer

- No commitear `.env` (está en `.gitignore`; revisa `git status` antes de `git add`).
- No activar `VENTANA_AGENT_BACKEND=stub` "para probar rápido" y dejarlo puesto — ocultó 4 bugs en Sprint-01 y 5 más en la verificación con claves reales (ver `MEMORY.md`).
- No cambiar `agent.py`/`tools.py` para "forzar" el modo real: el default ya es real.
