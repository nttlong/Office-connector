import logging
import threading
from os import path
from time import sleep
from pkg_resources import Requirement
from pkg_resources import resource_filename

# 3rd party modules
from win32api import GetModuleHandle
from win32api import PostQuitMessage
from win32con import CW_USEDEFAULT
from win32con import IDI_APPLICATION
from win32con import IMAGE_ICON
from win32con import LR_DEFAULTSIZE
from win32con import LR_LOADFROMFILE
from win32con import WM_DESTROY
from win32con import WM_USER
from win32con import WS_OVERLAPPED
from win32con import WS_SYSMENU
from win32gui import CreateWindow
from win32gui import DestroyWindow
from win32gui import LoadIcon
from win32gui import LoadImage
from win32gui import NIF_ICON
from win32gui import NIF_INFO
from win32gui import NIF_MESSAGE
from win32gui import NIF_TIP
from win32gui import NIM_ADD
from win32gui import NIM_DELETE
from win32gui import NIM_MODIFY
from win32gui import RegisterClass
from win32gui import UnregisterClass
from win32gui import Shell_NotifyIcon
from win32gui import UpdateWindow
from win32gui import WNDCLASS
from win32gui import NIIF_NOSOUND
from win10toast import ToastNotifier
def __show_toast_no_sound__(self, title, msg,
                icon_path, duration):
    """Notification settings.

    :title: notification title
    :msg: notification message
    :icon_path: path to the .ico file to custom notification
    :duration: delay in seconds before notification self-destruction
    """
    message_map = {WM_DESTROY: self.on_destroy, }

    # Register the window class.
    self.wc = WNDCLASS()
    self.hinst = self.wc.hInstance = GetModuleHandle(None)
    self.wc.lpszClassName = str("PythonTaskbar")  # must be a string
    self.wc.lpfnWndProc = message_map  # could also specify a wndproc.
    try:
        self.classAtom = RegisterClass(self.wc)
    except:
        pass  # not sure of this
    style = WS_OVERLAPPED | WS_SYSMENU
    self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,
                             0, 0, CW_USEDEFAULT,
                             CW_USEDEFAULT,
                             0, 0, self.hinst, None)
    UpdateWindow(self.hwnd)

    # icon
    if icon_path is not None:
        icon_path = path.realpath(icon_path)
    else:
        icon_path = resource_filename(Requirement.parse("win10toast"), "win10toast/data/python.ico")
    icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
    try:
        hicon = LoadImage(self.hinst, icon_path,
                          IMAGE_ICON, 0, 0, icon_flags)
    except Exception as e:
        logging.error("Some trouble with the icon ({}): {}"
                      .format(icon_path, e))
        hicon = LoadIcon(0, IDI_APPLICATION)

    # Taskbar icon
    flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
    nid = (self.hwnd, 0, flags, WM_USER + 20, hicon, "Tooltip")
    Shell_NotifyIcon(NIM_ADD, nid)
    Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,
                                  WM_USER + 20,
                                  hicon, "Balloon Tooltip", msg, 200,
                                  title, NIIF_NOSOUND))
    # take a rest then destroy
    sleep(duration)
    DestroyWindow(self.hwnd)
    UnregisterClass(self.wc.lpszClassName, None)
    return None

old_handler = getattr(ToastNotifier, "on_destroy")
def on_toast_destroy(toaster, hwnd, msg, wparam, lparam):
    old_handler(toaster, hwnd, msg, wparam, lparam)
    return 0
setattr(ToastNotifier,"on_destroy",on_toast_destroy)
setattr(ToastNotifier,"show_toast_no_sound",__show_toast_no_sound__)