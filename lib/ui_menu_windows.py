import lib.ui_menu_abstraction
from PyQt5.QtWidgets import QMenu, QAction, QApplication
import lib.loggers
import sys
import os
class Menu(lib.ui_menu_abstraction.BaseMenu):
    def build_menu(self,menu):
        action_setting = QAction("Setting ...", menu)
        action_exit = QAction("Exit", menu)
        menu.addAction(action_setting)
        menu.addAction(action_exit)


        def handle_action_exit():
            import lib.ui_controller
            try:
                lib.ui_controller.loader.get_main_app().quit()
                os._exit(0)
            except:
                sys.exit()

        action_exit.triggered.connect(handle_action_exit)