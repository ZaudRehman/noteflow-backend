from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, List[WebSocket]] = {}

    async def connect(self, note_id: str, websocket: WebSocket):
        await websocket.accept()
        if note_id not in self.active_connections:
            self.active_connections[note_id] = []
        self.active_connections[note_id].append(websocket)

    def disconnect(self, note_id: str, websocket: WebSocket):
        self.active_connections[note_id].remove(websocket)
        if not self.active_connections[note_id]:
            del self.active_connections[note_id]

    async def broadcast(self, note_id: str, message: str, sender: WebSocket):
        for connection in self.active_connections.get(note_id, []):
            if connection != sender:
                await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/notes/{note_id}")
async def websocket_endpoint(websocket: WebSocket, note_id: str):
    await manager.connect(note_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(note_id, data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(note_id, websocket)