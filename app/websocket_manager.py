from fastapi import WebSocket
from typing import List, Optional

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.last_message: Optional[str] = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New connection: {websocket.client}. Total: {len(self.active_connections)}")
        if self.last_message:
            await websocket.send_text(self.last_message)
            print(f"Sent last message to new connection: {self.last_message}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Connection closed. Total: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        self.last_message = message
        print(f"Broadcasting message: '{message}' to {len(self.active_connections)} connection(s)")
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()