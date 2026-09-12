# PENDIENTES.md

**Para quien tenga las credenciales de OpenAI y/o Exa.** Esto es lo único que falta para que Ventana corra con el modelo y la verificación externa reales — no hay que tocar ni una línea de código.

---

## Qué está pendiente, exactamente

Sprint-01 y Sprint-02 están **completados y auditados** (ver `MEMORY.md`, `.sprints/SPEC-01.md`, `.sprints/SPEC-02.md`). Todo el flujo — indexado, propuesta de campos, aprobación, reintento ante `ref_not_found`, verificación de empresa/RUC — funciona hoy en **modo `stub`**: un agente determinista sin llamadas de red, que sigue exactamente el mismo contrato que el agente real (ver `docs/RIESGOS.md` R8).

Lo único que el modo `stub` no puede probar es que el modelo de OpenAI y la API de Exa respondan de verdad. Eso requiere las claves.

## Qué hacer (2 minutos)

1. En la carpeta `backend/`, copia la plantilla si aún no existe un `.env`:
   ```bash
   cd backend
   cp .env.example .env
   ```
2. Abre `.env` y pega tus claves:
   ```
   OPENAI_API_KEY=sk-...
   EXA_API_KEY=...
   ```
   (`OPENROUTER_API_KEY` es opcional — solo hace falta si el crédito de OpenAI se agota a mitad del evento; ver `docs/RIESGOS.md` R8.)
3. **No borres ni comentes** la línea `# VENTANA_AGENT_BACKEND=stub` del archivo — debe quedar **comentada** (con `#` delante). Si esa variable queda activa, el backend sigue en modo simulado aunque hayas puesto las claves.
4. Reinicia el backend:
   ```bash
   source .venv/bin/activate
   uvicorn main:app --port 8000
   ```
   Sin `VENTANA_AGENT_BACKEND=stub` en el entorno, el backend arranca en modo real por defecto — no hace falta ninguna otra bandera.

## Cómo verificar que ya está usando las claves de verdad

```bash
cd backend && source .venv/bin/activate
pytest tests/ -v
```

Con las claves puestas, la suite completa debe seguir en **44/44 Verde** (los tests fuerzan el modo `stub` donde corresponde, así que no dependen de la clave para pasar). La prueba real es esta, contra el backend ya corriendo:

```bash
curl -s -X POST localhost:8000/agent/turn -H 'Content-Type: application/json' -d '{
  "session_id": "s_check",
  "locale": "es",
  "message": "Solicitud de GRUPO ANDINO SAC con RUC 20456789123.",
  "page": {"url":"http://x","title":"t","elements":[
    {"ref":"e0","tag":"input","type":"text","label":"Razon social de la empresa","value":"","options":null,"required":false}
  ]},
  "action_results": null
}' | python3 -m json.tool
```

Mira el campo `trace`:
- Si dice `"stub: match for '...'"` → todavía está en modo simulado (revisa el paso 3).
- Si dice `"exa: found — ..."` o `"exa: not found — ..."` → **la clave de Exa ya está funcionando de verdad.**

Para confirmar la clave de OpenAI, prueba el mismo `curl` con un mensaje real y observa que `reply` y cada `reason` los redacta el modelo (en modo `stub` esas frases son siempre las mismas plantillas fijas; con la clave real, el texto varía según lo que escribas).

## Qué NO hay que hacer

- No commitear el archivo `.env` — ya está en `.gitignore`, pero revisa `git status` antes de cualquier `git add`.
- No cambiar el código de `agent.py`/`tools.py` para "forzar" el modo real — el default ya es real; si algo falla, es la clave o la cuenta, no el código.
- No activar `VENTANA_AGENT_BACKEND=stub` "para probar más rápido" y dejarlo puesto — es exactamente el error que ocultó dos bugs reales en la primera auditoría de Sprint-01 (ver `MEMORY.md`).

## Si algo falla

- **`model_error` en la respuesta:** la clave de OpenAI no es válida o no tiene crédito. El backend degrada con elegancia (nunca rompe el panel) — revisa `backend/.env`.
- **Exa no encuentra nada esperado:** normal si el nombre de la empresa de tu prueba no existe realmente — `verify_entity` refleja lo que Exa encuentra de verdad, no un resultado fijo.
- Cualquier duda, el flujo completo end-to-end (indexado → propuesta → aprobación → escritura real en el DOM) ya está probado en Chrome real sin necesidad de estas claves — así que si algo no funciona al conectarlas, el problema está acotado a la integración con el proveedor, no al resto del sistema.
