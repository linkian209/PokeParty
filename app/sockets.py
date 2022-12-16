from collections import defaultdict
from typing import Dict
from fastapi import WebSocket
from uuid import UUID


class ConnectionManager:
    def __init__(self):
        self.active_connections: defaultdict[int, Dict[UUID, WebSocket]] = defaultdict(None)

    async def connect(self, websocket: WebSocket, client_id: int, socket_id: UUID):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = dict()
        self.active_connections[client_id][socket_id] = websocket

    def disconnect(self, client_id: int, socket_id: UUID):
        if client_id in self.active_connections and socket_id in self.active_connections[client_id]:
            del self.active_connections[client_id][socket_id]
            if len(self.active_connections[client_id].keys()) == 0:
                del self.active_connections[client_id]

    async def send_json(self, message: dict, client_id: int):
        if client_id in self.active_connections:
            for socket in self.active_connections[client_id]:
                await self.active_connections[client_id][socket].send_json(message)

manager = ConnectionManager()