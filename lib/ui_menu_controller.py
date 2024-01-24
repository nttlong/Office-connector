import lib.ui_menu_abstraction
loader: lib.ui_menu_abstraction.BaseMenu = None
import lib.config

if lib.config.get_os_name()==lib.config.OSEnum.windows:
    import lib.ui_menu_windows
    loader = lib.ui_menu_windows.Menu()