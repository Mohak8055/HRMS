from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from app.kafka_producer import send_message
from app.utils.auth import allow_roles
from app.websocket_manager import manager

router = APIRouter()

@router.post("/broadcast", dependencies=[Depends(allow_roles(["Admin"]))])
async def broadcast_message(message: dict):
    send_message('broadcast_messages', message)
    return {"message": "Broadcast message sent."}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)