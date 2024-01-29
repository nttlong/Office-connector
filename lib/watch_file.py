import pathlib
import threading
import time
import uuid

import requests.exceptions
from watchdog.observers import Observer
from lib.controller_file import on_edit
import lib.config
from watchdog.events import FileSystemEventHandler
import lib.cacher_tracking
tracking={}
import lib.loggers
import lib.contents
import lib.ui_controller
import os
lock = threading.Lock()
class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        def run():
            if hasattr(event,"event_type") and event.event_type=="deleted":
                return
            lib.loggers.logger.info(event.src_path)
            if not os.path.isfile(event.src_path):
                return


            track_file =os.sep.join ([lib.config.get_app_track_dir(), event.src_path[len(lib.config.get_app_data_dir()):]])
            file_name = pathlib.Path(event.src_path).stem
            if not (len(file_name) == 64 and all(c in "0123456789abcdef" for c in file_name)):
                return
            info = lib.contents.get_info_by_id(id=file_name,track_file=track_file)
            if info is None:
                return
            has_change = info.is_change()
            if has_change:
                info.status=lib.contents.DownLoadInfoEnum.Unknown


                try:
                    lock.acquire()
                    ret_upload = info.do_upload()
                    if ret_upload:
                    # Critical section protected by the lock
                        info.commit_change()
                        info.save_commit()
                        lib.ui_controller.loader.show_message("File updated")
                except requests.exceptions.HTTPError as e:
                    lib.ui_controller.loader.show_message_error(
                        f"Save file to {info.check_in_url} was fail\n"
                        f"Http Error {e.response.status_code}"
                    )
                except Exception as e:
                    # Handle the exception without releasing the lock yet
                    lib.ui_controller.loader.show_message_error(f"Application try to save file but got error")
                finally:
                    # Always release the lock, even if an exception occurs
                    lock.release()





        run()
        # try:
        #     run()
        # except  Exception as e:
        #     lib.loggers.logger.error(e)


def do_watch_file():
    observer = Observer()
    observer.schedule(MyHandler(), lib.config.app_data_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()