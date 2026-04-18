from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from core.session_store import sessions
from schemas.session_schema import CreateSessionRequest, JoinSessionRequest
from services.session_service import (
    create_session_service,
    join_session_service,
    save_vote,
    reveal_votes,
    reset_votes,
    get_session_state
)
from websocket.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

# =========================
# REST endpoints
# =========================

@router.post("/session/create")
def create_session(data: CreateSessionRequest):
    return create_session_service(data.name)


@router.post("/session/join")
def join_session(data: JoinSessionRequest):
    return join_session_service(data.code, data.name)


# =========================
# WebSocket
# =========================

@router.websocket("/ws/{code}")
async def websocket_endpoint(websocket: WebSocket, code: str):
    print("Conectando ao WS...")

    # valida sessão antes de conectar
    if code not in sessions:
        await websocket.close()
        return

    await manager.connect(code, websocket)
    print("WS conectado com sucesso!")

    # envia estado inicial
    state = get_session_state(code)
    await websocket.send_text(json.dumps({
        "type": "state",
        "data": state
    }))

    try:
        while True:
            try:
                data = await websocket.receive_text()
            except:
                break  # conexão pode ter caído

            # tenta converter JSON
            try:
                message = json.loads(data)
            except:
                continue

            # pega tipo da mensagem com segurança
            msg_type = message.get("type")
            user = message.get("user")

            # =========================
            # regras de negócio
            # =========================

            if msg_type == "vote":
                value = message.get("value")

                # validações básicas
                if not user or not isinstance(value, int):
                    continue

                save_vote(code, user, value)

            elif msg_type == "reveal":
                reveal_votes(code)

            elif msg_type == "reset":
                reset_votes(code)

            elif msg_type == "sync":
                pass

            # =========================
            # broadcast do estado
            # =========================

            state = get_session_state(code)

            await manager.broadcast(code, json.dumps({
                "type": "state",
                "data": state
            }))

    except WebSocketDisconnect:
        print("WS desconectado")
        manager.disconnect(code, websocket)