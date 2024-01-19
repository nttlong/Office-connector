import asyncio

import websockets
import win32com.client

import lib.contents
import lib.controllers


async def handler(websocket, path: str):
    url = path.split("=")[1]

    ret = await lib.controllers.resolve_async(websocket, request_path=path, url_file=url)
    await websocket.send(ret)


async def server_async():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Run forever until stopped


def start_server():
    asyncio.run(server_async())
