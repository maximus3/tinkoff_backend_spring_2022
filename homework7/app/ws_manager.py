from asyncio import Lock

from fastapi import WebSocket


class WSManager:
    def __init__(self) -> None:
        self.connections: list[WebSocket] = []
        self.lock = Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self.lock:
            self.connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self.lock:
            self.connections.remove(websocket)
            await websocket.close()

    async def broadcast(self, message: str) -> None:
        async with self.lock:
            for connection in self.connections:
                await connection.send_text(message)


ws_manager = WSManager()
