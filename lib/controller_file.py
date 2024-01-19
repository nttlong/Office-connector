from  watchdog.events import FileSystemEvent,FileClosedEvent,FileOpenedEvent,FileModifiedEvent
def on_edit(src_path:str,app_name:str,upload_id:str):
    print(src_path)
    print(app_name)
    print(upload_id)
