import lib.sys_abtraction


loader: lib.sys_abtraction.BaseSys = None

import lib.config

if lib.config.get_os_name()==lib.config.OSEnum.windows:
    import lib.sys_windows
    loader = lib.sys_windows.SysOs()