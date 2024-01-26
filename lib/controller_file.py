from watchdog.events import FileSystemEvent, FileClosedEvent, FileOpenedEvent, FileModifiedEvent
import lib.cacher_tracking
import lib.config
import lib.contactor
import lib.contents
def on_edit(src_path: str, app_name: str, upload_id: str):
    info = lib.contents.get_info_by_id(upload_id)
    if not isinstance(info,lib.contents.DownLoadInfo):
        return
    ret = lib.contactor.do_upload(
        app_name=app_name,
        upload_id=upload_id,
        src_path=src_path,
        info=info
    )
    return ret


