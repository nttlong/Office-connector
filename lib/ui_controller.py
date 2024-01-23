import lib.ui_abstractions


loader: lib.ui_abstractions.BaseLoader = None

import lib.config

if lib.config.get_os_name()==lib.config.OSEnum.windows:
    import lib.ui_windows
    loader = lib.ui_windows.Loader()
