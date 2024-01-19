import io
import sys

import extract_icon
import pystray
from PIL import Image


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
            sys.exit()  # Exit the application
        except Exception as e:
            print(e)
            pass
        finally:
            sys.exit()

    # Load your icon
    menu = pystray.Menu(
        pystray.MenuItem("Show Window", show_window),
        pystray.MenuItem("Exit", exit_app),
    )
    icon = pystray.Icon("Codx Office interact", icon, menu=menu)
    return icon.run
