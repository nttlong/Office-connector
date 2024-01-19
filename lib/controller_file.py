from watchdog.events import FileSystemEvent, FileClosedEvent, FileOpenedEvent, FileModifiedEvent
import lib.cacher_tracking
import lib.config
import lib.contactor
def on_edit(src_path: str, app_name: str, upload_id: str):
    info = lib.cacher_tracking.host.get(src_path)
    if not isinstance(info,lib.config.UploadInfo):
        return
    if not info.is_in_upload:
        lib.contactor.do_upload(
            app_name=app_name,
            upload_id=upload_id,
            src_path=src_path,
            info=info
        )


    print(src_path)
    print(app_name)
    print(upload_id)
