# This is a sample Python script.
# how to build
# pyinstaller --onefile E:\long\python\codx.py --icon=E:\long\python\icon\WP.ico --noconsole
import pathlib
import threading
import time
import uuid
import extract_icon


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.





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
    # start_server_thread=threading.Thread(target=start_server)
    # start_server_thread.name="Socket"
    tray_icon_run_thread=threading.Thread(target=tray_icon_run)
    tray_icon_run_thread.name="Tray"
    tray_icon_run_thread.start()
    # th1.start()


    # th1.join()
    start_server()
    tray_icon_run_thread.join()
    # threading.Thread(target=tray_icon_run).start()
    #
    # start_socket()
except Exception as e:
    txt = traceback.print_exc()
    print(__file__)
    print(txt)
    # time.sleep(10000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
