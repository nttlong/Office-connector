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
import urllib3
import json
import lib.ui_controller
async def handler(websocket):

    try:


        async for message in websocket:
            data = json.loads(message)
            check_data = lib.controllers.check_data(data)
            if check_data.get("error_code"):
                lib.ui_controller.loader.show_message_error(check_data["error_message"])
                await lib.controllers.send_error_to_client(websocket=websocket, error_code="system",
                                                           error_message="System error")
            ret = await lib.controllers.resolve_async(websocket, check_data)
            if ret is None:
                await websocket.send("error")
                return
            id = ret.id


    except lib.errors.Error as e:
        lib.ui_controller.loader.show_message_error(e.message)
        await lib.controllers.send_error_to_client(websocket=websocket, error_code="system",error_message="System error")

    except Exception as e:
        raise e
        # lib.ui_controller.loader.show_message_error(str(e))
        # await lib.controllers.send_error_to_client(websocket=websocket,error_code="system", error_message="System error")

async def server_async():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Run forever until stopped


def start_server():
    asyncio.run(server_async())
