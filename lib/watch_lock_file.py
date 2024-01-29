import datetime
import os
import pathlib
import time
import uuid

import lib.sys_controller
import lib.config
import lib.contents
import lib.loggers
def watcher():
    app_data_dir = lib.config.get_app_data_dir()
    while True:
        list_of_files = lib.sys_controller.loader.get_list_of_files(app_data_dir)
        for x in list_of_files:
            try:
                t= os.path.getmtime(x)
                fx = datetime.datetime.fromtimestamp(t)
                file_id = pathlib.Path(x).stem
                if (datetime.datetime.now()-fx).seconds>30*60:
                    if not (len(file_id) == 64 and all(c in "0123456789abcdef" for c in file_id)):
                        return
                    if not lib.sys_controller.loader.is_file_in_use(file_path=x):

                        lib.sys_controller.loader.delete_file(file_path=x)
                        lib.loggers.logger.info(f"delete {x}")
                        lib.sys_controller.loader.delete_file(os.path.join(lib.config.get_app_track_dir(), file_id))
                        lib.loggers.logger.info(f"delete {os.path.join(lib.config.get_app_track_dir(), file_id)}")
                        if lib.contents.__cache__.get(file_id):
                            del lib.contents.__cache__[file_id]


            except:
                continue
            time.sleep(0.5)
        time.sleep(0.5)

