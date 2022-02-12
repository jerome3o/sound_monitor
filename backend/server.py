import asyncio

from typing import List
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from uvicorn import Config, Server


import time

from backend.sound import init_stream


app = FastAPI()


def make_iter():
    queue = asyncio.Queue()
    def put(data):
        loop.call_soon_threadsafe(queue.put_nowait, data)
        return ()
    async def get():
        while True:
            yield await queue.get()

    return get(), put

_get, _put = make_iter()
stream = init_stream(_put)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async for data in _get:
        await websocket.send_text(str(max(abs(data))))


loop = asyncio.get_event_loop()
config = Config(app=app, loop=loop)
stream.start_stream()
server = Server(config=config)



if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    loop.run_until_complete(server.serve())