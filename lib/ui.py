import io
import os
import sys

import extract_icon
import pystray
from PIL import Image
import win32api
import win32con
import logging

logging.basicConfig(filename="codx.log", level=logging.ERROR)


def get_icon():
    icon_extractor = extract_icon.ExtractIcon(sys.executable)
    raw = icon_extractor.get_raw_windows_preferred_icon()
    icon_io = io.BytesIO(raw)
    app_icon = Image.open(icon_io)
    return app_icon


def create_tray_icon(icon):
    def show_window():
        # Code to display your application's main window
        pass

    def exit_app():
        try:
            # start_server.ws_server.server.close()
            icon.stop()  # Stop the tray icon
            os._exit(0)
        except Exception as e:
            logging.error(e)
            os._exit(0)
        finally:
            sys.exit()

    # Load your icon
    menu = pystray.Menu(
        pystray.MenuItem("Show Window", show_window),
        pystray.MenuItem("Exit", exit_app),
    )
    icon = pystray.Icon("Codx Office interact", icon, menu=menu)
    return icon.run


def show_message_error(message):
    try:
        title = "Codx message"
        win32api.MessageBox(0, message, title, win32con.MB_OK)
    except Exception as e:
        logging.error(e)
