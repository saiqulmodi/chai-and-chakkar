import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
from collections import defaultdict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "server.log"

# Configure rotating file handler (1 MB max, 3 backups)
file_handler = RotatingFileHandler(
    LOG_PATH, maxBytes=1_048_576, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)

logger = logging.getLogger("chai_chakkar_ws")

# pythonw.exe has sys.stdout/sys.stderr set to None; redirect to log file so Uvicorn never crashes
if sys.stdout is None:
    sys.stdout = open(LOG_PATH, "a", encoding="utf-8", buffering=1)
if sys.stderr is None:
    sys.stderr = open(LOG_PATH, "a", encoding="utf-8", buffering=1)

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
    logger.info("Client joined room %s (peers=%d)", code, len(rooms[code]))
    try:
        while True:
            raw = await websocket.receive_text()
            for peer in list(rooms[code]):
                if peer is not websocket:
                    try:
                        await peer.send_text(raw)
                    except Exception as exc:
                        logger.warning("Failed sending to peer in %s: %s", code, exc)
                        rooms[code].discard(peer)
    except WebSocketDisconnect:
        rooms[code].discard(websocket)
        logger.info("Client left room %s (peers=%d)", code, len(rooms[code]))
        if not rooms[code]:
            rooms.pop(code, None)

if __name__ == "__main__":
    logger.info("Starting Chai & Chakkar WebSocket Relay on 0.0.0.0:8765")
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8765,
        reload=False,
        log_config=None,  # Route Uvicorn logs cleanly into root_logger -> server.log
    )
