import pathlib
import time
import uuid

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
            app_name= pathlib.Path(event.src_path).parent.name
            oid=None
            try:
                oid=uuid.UUID(file_name)
            except:
                return
            info = lib.contents.get_info_by_id(id=str(oid),track_file=track_file)
            if info is None:
                return
            has_change = info.is_change()
            if has_change:
                info.status=lib.contents.DownLoadInfoEnum.Unknown
                ret_upload = info.do_upload()
                if ret_upload:
                    info.commit_change()
                    info.save_commit()
                    lib.ui_controller.loader.show_message("File updated")


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