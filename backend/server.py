import asyncio
import json

from typing import List
from fastapi import FastAPI, WebSocket
from uvicorn import Config, Server


import numpy as np

from backend.sound import calculate_max_amplitude, calculate_psd, init_stream


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


_ws_list: List[WebSocket] = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    _ws_list.append(websocket)

    while True:
        await websocket.receive_text()


def _get_data_packet(data: np.array):
    return {
        "spectra": calculate_psd(data),
        "max_amplitude": calculate_max_amplitude(data),
    }


async def transmit_data():
    async for data in _get:
        for ws in _ws_list:
            try:
                await ws.send_text(json.dumps(_get_data_packet(data)))
            except Exception:
                _ws_list.remove(ws)


loop = asyncio.get_event_loop()
loop.create_task(transmit_data())
config = Config(app=app, loop=loop, host="0.0.0.0")
stream.start_stream()
server = Server(config=config)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    loop.run_until_complete(server.serve())
