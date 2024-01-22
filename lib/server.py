import asyncio
import pathlib

import websockets
import win32com.client

import lib.contents
import lib.controllers
import lib.config
import lib.errors
import lib.ui
import lib.cacher_tracking
async def handler(websocket, path: str):

    try:
        url = path.split("=")[1]
        upload_info= lib.config.get_app_config(url)
        ret = await lib.controllers.resolve_async(websocket, request_path=path, url_file=url,upload_info=upload_info)
        id= ret.upload_id
        lib.cacher_tracking.host[id]=upload_info


        await websocket.send(ret)
    except lib.errors.Error as e:
        lib.ui.show_message_error(e.message)
        await websocket.send("error")


async def server_async():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Run forever until stopped


def start_server():
    asyncio.run(server_async())
