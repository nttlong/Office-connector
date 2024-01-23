import enum
import os
import pathlib
import time
import uuid
import traceback
import lib.loggers
import urllib3

import lib.errors
import platform

from enum import Enum

app_dir_name = "Codx-Desktop-Connector"
data_dir_name = "data"
log_track_dir = "tracks"

class OSEnum(enum.Enum):
    unknown = "unknown"
    windows = "Windows"
    macos = "Darwin"
    linux = "Linux"


def get_os_name() -> OSEnum:
    os_name = platform.system()
    if os_name == "Windows":
        return OSEnum.windows
    elif os_name == "Darwin":
        return OSEnum.macos
    elif os_name == "Linux":
        return OSEnum.linux
    else:
        return OSEnum.unknown


def get_app_data_local() -> str:
    if get_os_name() == OSEnum.windows:
        return os.path.expanduser("~\\AppData\\Local")
    elif get_os_name() == OSEnum.macos:
        return os.path.expanduser("~/Library/Application Support/")


def get_app_data_dir() -> str:
    ret = os.path.join(get_app_data_local(), app_dir_name, data_dir_name)
    os.makedirs(ret, exist_ok=True)
    return ret
def get_app_track_dir() -> str:
    ret = os.path.join(get_app_data_local(), app_dir_name, log_track_dir)
    os.makedirs(ret, exist_ok=True)
    return ret

def get_app_dir() -> str:
    ret = os.path.join(get_app_data_local(), app_dir_name)
    os.makedirs(ret, exist_ok=True)
    return ret


app_dir = get_app_dir()
app_data_dir = get_app_data_dir()


class UploadInfo:
    app_name: str
    upload_id: str
    file_name_only: str
    file_ext: str
    scheme: str
    host: str
    port: str
    is_in_upload: bool


def get_app_config(url: str) -> UploadInfo:
    try:
        ret = urllib3.util.url.parse_url(url)
        app_name_pos_start = ret.path.index("/api/") + len("/api/")
        app_name_pos_end = ret.path.index("/", app_name_pos_start)
        app_name = ret.path[app_name_pos_start:app_name_pos_end]
        start_id_pos = ret.path.index("/", app_name_pos_end + 1) + 1
        end_id_pos = ret.path.index("/", start_id_pos + 1)
        id = ret.path[start_id_pos:end_id_pos]
        check_id = uuid.UUID(id)
        ret_info = UploadInfo()
        ret_info.app_name = app_name
        ret_info.upload_id = id
        file_name_only = pathlib.Path(ret.path).stem
        file_ext = pathlib.Path(ret.path).suffix
        if file_ext is None or file_ext == "":
            raise lib.errors.Error("Invalid file")
        else:
            file_ext = file_ext[1:]
        ret_info.file_ext = file_ext.lower()
        ret_info.file_name_only = file_name_only
        ret_info.scheme = ret.scheme
        ret_info.host = ret.host
        if ret.port:
            ret_info.port = str(ret.port)
        else:
            ret_info.port = None
        ret_info.is_in_upload = False

        return ret_info
    except ValueError as e:
        raise lib.errors.Error("Invalid Codx server")
    except Exception as e:
        raise lib.errors.Error(type(e).__name__)
