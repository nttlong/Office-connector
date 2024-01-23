import pathlib
import time
import uuid

import lib.sys_controller
import lib.config
import lib.contents

def watcher():
    app_data_dir = lib.config.get_app_data_dir()
    while True:
        list_of_files = lib.sys_controller.loader.get_list_of_files(app_data_dir)
        for x in list_of_files:
            file_id = pathlib.Path(x).stem
            try:
                odi = uuid.UUID(file_id)
                if not lib.sys_controller.loader.is_file_in_use(file_path=x):
                    lib.sys_controller.loader.delete_file(file_path=x)
                    if lib.contents.__cache__.get(file_id):
                        del lib.contents.__cache__[file_id]
            except:
                continue
            time.sleep(0.5)


