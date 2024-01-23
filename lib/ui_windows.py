import pathlib

import lib.ui_abstractions
import win32com.client


class Loader(lib.ui_abstractions.BaseLoader):

    def load_word(self, file_path: str):
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = True  # Make Word window visible
        doc = word.Documents.Open(file_path)
        word.Activate()  # This brings Word to the foreground



    def load_power_point(self, file_path):
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = True  # Make Word window visible
        doc = presentation = powerpoint.Presentations.Open(file_path)
        powerpoint.Activate()  # This brings Word to the foreground

    def load_excel(self, file_path):
        excel = win32com.client.Dispatch("Excel.Application")
        workbook = excel.Workbooks.Open(file_path)
        excel.Visible = True
        workbook.Activate()

    def load_note_pad(self, file_path):
        import subprocess
        subprocess.Popen(["notepad", file_path])

    def load_paint_app(self, file_path):
        import subprocess
        subprocess.Popen(["MSPaint", file_path])

    def show_message_error(self, message):
        import win32api
        import win32con
        import lib.contents
        title = lib.contents.get_app_name()
        win32api.MessageBox(0, message, title, win32con.MB_OK)
    def set_auto_start_up(self):
        import winreg
        import lib.contents
        import sys
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        winreg.SetValueEx(key, lib.contents.get_app_name(), 0, winreg.REG_SZ, sys.executable)

    def create_tray_icon(self,icon):
        import lib.contents
        import os
        import sys
        import lib.contents
        import pystray
        def show_window():
            # Code to display your application's main window
            pass

        def exit_app():
            try:
                # start_server.ws_server.server.close()
                icon.stop()  # Stop the tray icon
                os._exit(0)
            except Exception as e:
                lib.loggers.logger.error(e)
                os._exit(0)
            finally:
                sys.exit()

        # Load your icon
        menu = pystray.Menu(
            pystray.MenuItem("Show Window", show_window),
            pystray.MenuItem("Exit", exit_app),
        )
        icon = pystray.Icon(lib.contents.get_app_name(), icon, menu=menu)
        return icon.run

    def get_icon(self):
        import extract_icon
        import sys
        import io
        from PIL import Image
        icon_extractor = extract_icon.ExtractIcon(sys.executable)
        raw = icon_extractor.get_raw_windows_preferred_icon()
        icon_io = io.BytesIO(raw)
        app_icon = Image.open(icon_io)
        return app_icon