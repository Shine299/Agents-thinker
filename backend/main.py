"""FastAPI entrypoint. See docs/API_CONTRACTS.md — frozen at 11:15, do not
renegotiate the shape here.

Every outcome of /agent/turn, failures included, is a TurnResponse: the panel
has exactly one shape to parse (contract rule: the backend answers
status "error" with a readable message, never a stack trace).
"""

import asyncio
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent import error_response, run_turn
from contracts import TurnRequest, TurnResponse

# Keys live in backend/.env (see .env.example). Resolved next to this file so
# it works no matter where uvicorn is launched from.
load_dotenv(Path(__file__).with_name(".env"))

app = FastAPI(title="Ventana backend")

# The panel is an extension page, so its requests are cross-origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 8s was calibrated on the stub; the real model needs ~8s for the 10-field demo
# case (11 tool calls). 20s keeps headroom without letting a hung call wait forever.
TURN_TIMEOUT_SECONDS = 20


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/agent/turn", response_model=TurnResponse)
async def agent_turn(request: TurnRequest):
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(run_turn, request), timeout=TURN_TIMEOUT_SECONDS
        )
    except asyncio.TimeoutError:
        return error_response(
            request.session_id,
            request.locale,
            "timeout",
            f"timeout after {TURN_TIMEOUT_SECONDS}s",
        )
