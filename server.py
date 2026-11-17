from collections import defaultdict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Chai & Chakkar Multiplayer Relay")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms: dict[str, set[WebSocket]] = defaultdict(set)

@app.get("/health")
async def health():
    return {"status": "ok", "active_rooms": len(rooms)}

@app.websocket("/ws/{room_code}")
async def websocket_room(websocket: WebSocket, room_code: str):
    code = room_code.strip().upper()[:12]
    await websocket.accept()
    rooms[code].add(websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            for peer in list(rooms[code]):
                if peer is not websocket:
                    try:
                        await peer.send_text(raw)
                    except Exception:
                        rooms[code].discard(peer)
    except WebSocketDisconnect:
        rooms[code].discard(websocket)
        if not rooms[code]:
            rooms.pop(code, None)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8765, reload=False)
