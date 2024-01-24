import pathlib

import lib.ui_abstractions
import win32com.client


def com_error_wrapper(client_app_name: str):
    import pywintypes
    import lib.loggers
    def wrapper(*args, **kwargs):
        caller = args[0]

        def re_call(*args, **kwargs):
            try:
                return caller(*args, **kwargs)
            except pywintypes.com_error as err:
                import win32api
                import win32con
                import lib.contents

                title = lib.contents.get_app_name()
                win32api.MessageBox(0, f"{client_app_name} is not installed or something wrong. Please install it to "
                                       f"proceed.",
                                    lib.contents.get_app_name(), win32con.MB_OK)
                lib.loggers.logger.error(err)
            except Exception as e:

                lib.loggers.logger.error(e)

        return re_call

    return wrapper


class Loader(lib.ui_abstractions.BaseLoader):

    def __init__(self):
        from win10toast import ToastNotifier
        self.qt_app_icon = None
        self.icon_raw_data = None
        self.icon_q_pixmap = None
        self.main_ui_app = None
        self.main_widget = None
        old_handler = getattr(ToastNotifier, "on_destroy")
        def on_toast_destroy(toaster, hwnd, msg, wparam, lparam):
            old_handler(toaster, hwnd, msg, wparam, lparam)
            return 0
        setattr(ToastNotifier,"on_destroy",on_toast_destroy)
        self.toaster = ToastNotifier()


    def get_main_app(self):
        return self.main_ui_app
    @com_error_wrapper("Microsoft Word")
    def load_word(self, file_path: str):
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = True  # Make Word window visible
        doc = word.Documents.Open(file_path)
        word.Activate()  # This brings Word to the foreground

    @com_error_wrapper("PowerPoint")
    def load_power_point(self, file_path):
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = True  # Make Word window visible
        doc = presentation = powerpoint.Presentations.Open(file_path)
        powerpoint.Activate()  # This brings Word to the foreground

    @com_error_wrapper("Excel")
    def load_excel(self, file_path):
        excel = win32com.client.Dispatch("Excel.Application")
        workbook = excel.Workbooks.Open(file_path)
        excel.Visible = True
        workbook.Activate()

    @com_error_wrapper("Notepad")
    def load_note_pad(self, file_path):
        import subprocess
        subprocess.Popen(["notepad", file_path])

    @com_error_wrapper("MS Paint")
    def load_paint_app(self, file_path):
        import subprocess
        subprocess.Popen(["MSPaint", file_path])

    def get_q_pixmap_app_icon(self):
        if self.icon_q_pixmap:
            return self.icon_q_pixmap
        else:
            from PyQt5.QtCore import Qt
            from PyQt5.QtGui import QImage, QPixmap
            image = QImage()
            image.loadFromData(self.get_icon_data())
            pixmap = QPixmap(image).scaledToHeight(32, Qt.SmoothTransformation)
            self.icon_q_pixmap = pixmap
            return self.icon_q_pixmap

    def show_message_error(self, param):

        import lib.config


        self.toaster.show_toast(lib.config.app_name, msg=param,
                           icon_path= self.get_app_icon_path(),
                           duration=5)  # Duration in seconds (optional)
    def show_message_error_delete(self, param):
            import lib.config
            from PyQt5.QtWidgets import QMessageBox
            msg_box = QMessageBox()
            from PyQt5.QtCore import Qt
            msg_box.setWindowFlags( Qt.WindowStaysOnTopHint)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle(lib.config.app_name)
            msg_box.setText(param)
            # def handle_accepted():
            #     # Do something specific when the user clicks "OK" or other positive button
            #     pass
            # msg_box.accepted.connect(handle_accepted)

            # msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            msg_box.deleteLater() # Can use exec_() here as the signal will prevent closure

    def set_auto_start_up(self):
        import winreg
        import lib.contents
        import sys
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        winreg.SetValueEx(key, lib.contents.get_app_name(), 0, winreg.REG_SZ, sys.executable)

    def create_tray_icon(self, icon):

        pass

    def get_icon(self):
        import io
        from PIL import Image
        icon_io = io.BytesIO(self.get_icon_data())
        app_icon = Image.open(icon_io)
        return app_icon

    def get_icon_data(self):
        import extract_icon
        import sys

        icon_extractor = extract_icon.ExtractIcon(sys.executable)
        raw = icon_extractor.get_raw_windows_preferred_icon()
        return raw

    def get_start_app(self):
        from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
        import lib.config
        import sys
        def running():
            app = QApplication([])  # Create a Qt application instance
            tray_icon = QSystemTrayIcon(self.get_qt_app_icon())
            self.main_widget = tray_icon
            menu = QMenu()
            action1 = QAction("Item 1", menu)
            action2 = QAction("Item 2", menu)
            menu.addAction(action1)
            menu.addAction(action2)
            tray_icon.setToolTip(lib.config.get_app_tooltip())
            tray_icon.setContextMenu(menu)
            tray_icon.show()
            self.main_ui_app = app
            app.setQuitOnLastWindowClosed(False)
            sys.exit(app.exec_())


        return running
    def get_app_icon_path(self):
        import os
        import lib.config
        icon_path= os.path.join(lib.config.get_app_dir(), "app.ico")
        if not os.path.isfile(icon_path):
            self.get_icon()
        return icon_path
    def get_qt_app_icon(self):
        if self.qt_app_icon:
            return self.qt_app_icon
        else:
            import os
            import lib.config
            from PyQt5.QtGui import QIcon
            icon_image = self.get_icon()
            icon_image.save(os.path.join(lib.config.get_app_dir(), "app.ico"))
            icon = QIcon(os.path.join(lib.config.get_app_dir(), "app.ico"))  # Load your icon
            self.qt_app_icon = icon
            return self.qt_app_icon
    def get_main_widget(self):
        return self.main_widget