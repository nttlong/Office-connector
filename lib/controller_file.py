from watchdog.events import FileSystemEvent, FileClosedEvent, FileOpenedEvent, FileModifiedEvent
import lib.cacher_tracking
import lib.config
import lib.contactor
import lib.contents
def on_edit(info:lib.contents.DownLoadInfo):

    ret = info.do_upload()
    return ret


