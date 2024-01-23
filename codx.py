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
def set_auto_start_up():
    import winreg
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
    winreg.SetValueEx(key, "Codx-Office-Client-Comunication", 0, winreg.REG_SZ, sys.executable)
if pathlib.Path(sys.executable).name=="codx":
    set_auto_start_up()

stop_server = False


import pystray
from PIL import Image
import sys
verion = 'p.0.1'
app_dir=pathlib.Path(__file__).parent.__str__()

server=None
start_server= None


from lib.server import server_async
from lib.ui import get_icon, create_tray_icon
from lib.server import start_server



try:
# In your main script, call this function to create the tray icon
    app_icon= get_icon()
    tray_icon_run=create_tray_icon(app_icon)

    tray_icon_run_thread=threading.Thread(target=tray_icon_run)
    tray_icon_run_thread.name="Tray"
    tray_icon_run_thread.start()

    watch_file_thread = threading.Thread(target=lib.watch_file.do_watch_file)
    watch_file_thread.start()
    start_server()
    tray_icon_run_thread.join()
    watch_file_thread.join()

except Exception as e:
    txt = traceback.print_exc()
    print(__file__)
    print(txt)
    # time.sleep(10000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
