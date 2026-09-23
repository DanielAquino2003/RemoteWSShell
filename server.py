import asyncio
import json
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from pty_manager import PTYManager


app = FastAPI()
INDEX_PATH = Path(__file__).with_name("index.html")


@app.get("/")
async def index():
    return FileResponse(INDEX_PATH)


async def websocket_to_pty(websocket, pty_session):
    while True:
        raw_message = await websocket.receive_text()
        message = json.loads(raw_message)

        if message.get("type") == "input":
            pty_session.write(message.get("data", "").encode())
        elif message.get("type") == "resize":
            rows = int(message["rows"])
            cols = int(message["cols"])
            if rows > 0 and cols > 0:
                pty_session.resize(rows, cols)


async def pty_to_websocket(websocket, pty_session):
    while True:
        output = await asyncio.to_thread(pty_session.read)
        await websocket.send_text(output.decode(errors="replace"))


@app.websocket("/terminal")
async def terminal(websocket: WebSocket):
    await websocket.accept()

    pty_session = PTYManager()
    pty_session.start()

    task_input = asyncio.create_task(websocket_to_pty(websocket, pty_session))
    task_output = asyncio.create_task(pty_to_websocket(websocket, pty_session))

    try:
        await asyncio.gather(task_input, task_output)
    except WebSocketDisconnect:
        pass
