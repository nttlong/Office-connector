import lib.thread_abtractions


loader: lib.thread_abtractions.BaseThreading = None

import lib.config

if lib.config.get_os_name()==lib.config.OSEnum.windows:
    import lib.thread_windows
    loader = lib.thread_windows.Loader()
