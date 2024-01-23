# This is a sample Python script.
# how to build
# pyinstaller --onefile E:\long\office-connector\Office-connector\codx.py --icon=E:\long\office-connector\Office-connector\icon\WP.ico --hidden-import=E:\long\office-connector\Office-connector\lib --noconsole
import pathlib
import threading
import time
import uuid
import extract_icon


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool Windows, actions, and settings.





# Press the green button in the gutter to run the script.
import asyncio
import websockets
import win32com.client
import requests
import os
import pystray
import pefile
import io
import traceback

import lib.contents
import sys
import lib.watch_file
import lib.ui


if pathlib.Path(sys.executable).name.lower()=="codx":
    import lib.ui_controller
    lib.ui_controller.loader.set_auto_start_up()


stop_server = False


import pystray
from PIL import Image
import sys
verion = 'p.0.1'
app_dir=pathlib.Path(__file__).parent.__str__()

server=None
start_server= None


from lib.server import server_async
from lib.server import start_server
import lib.ui_controller
import lib.loggers
import lib.thread_controller
import lib.watch_lock_file
def start_app():
    app_icon = lib.ui_controller.loader.get_icon()
    tray_icon_run = lib.ui_controller.loader.create_tray_icon(app_icon)
    tray_icon_run_thread= lib.thread_controller.loader.start(name="Tray", target=tray_icon_run, args=())
    watch_file_thread = lib.thread_controller.loader.start(name="wacth file", target=lib.watch_file.do_watch_file, args=())
    watch_lock_files_thread = lib.thread_controller.loader.start(name="watch_log_file",target=lib.watch_lock_file.watcher,args=())
    start_server()
    lib.thread_controller.loader.join([
        tray_icon_run_thread,
        watch_file_thread,
        watch_lock_files_thread
    ])

# start_app()
try:
# In your main script, call this function to create the tray icon
    start_app()

except Exception as e:
    lib.loggers.logger.error(e)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
