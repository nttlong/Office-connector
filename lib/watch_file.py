import pathlib
import time
import uuid

from watchdog.observers import Observer
from lib.controller_file import on_edit
import lib.config
from watchdog.events import FileSystemEventHandler
import lib.cacher_tracking
tracking={}
class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        file_name = pathlib.Path(event.src_path).stem
        app_name= pathlib.Path(event.src_path).parent.name
        try:
            oid=uuid.UUID(file_name)
        except:
            return
        if not lib.cacher_tracking.downloading.get(event.src_path):
            on_edit(src_path=event.src_path, upload_id=file_name,app_name=app_name)

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