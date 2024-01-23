import datetime
import enum
import math
import os
import pathlib
import typing
import uuid

import requests
import lib.data_hashing
from lib import config
import lib.cacher_tracking
import lib.loggers
import json

__cache__ = {}


def __json_converter__(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, DownLoadInfoEnum):
        return obj.value
    return obj


def __read_last_bytes__(file_path, n_bytes=1024):
    """
  Reads the last n_bytes of a file.

  Args:
      file_path: Path to the file.
      n_bytes: Number of bytes to read from the end (default: 1024).

  Returns:
      str: The last n_bytes of the file content.
  """
    file_size = os.path.getsize(file_path)
    seek_position = max(0, file_size - n_bytes)
    with open(file_path, "rb") as f:
        f.seek(seek_position)
        return f.read()


class DownLoadInfoEnum(enum.Enum):
    Ready = 1
    Unknown = 0


class DownLoadInfo:
    file_path: str
    app_name: str
    file_name_only: str
    file_ext: str
    scheme: str
    host: str
    port: str
    created_on: datetime.datetime
    size_in_bytes: int
    is_ready: bool
    is_sync: bool
    modify_time: typing.Optional[datetime.datetime]
    hash_contents: typing.Optional[typing.List[str]]
    download_dir: str
    size_in_bytes: int
    modify_time: str
    url: str
    id: str
    status: DownLoadInfoEnum

    def __init__(self, url: str):
        info = config.get_app_config(url)
        self.url = url
        self.download_dir = os.path.join(config.app_data_dir, info.app_name)
        file_name = info.upload_id
        os.makedirs(self.download_dir, exist_ok=True)

        self.file_path = os.path.join(self.download_dir, f"{file_name}.{info.file_ext}")
        self.id = pathlib.Path(self.file_path).stem

        self.is_in_download = False
        self.port = info.port
        self.scheme = info.scheme
        self.file_ext = info.file_ext
        self.app_name = info.app_name
        self.file_name_only = info.file_name_only
        self.host = info.host
        self.created_on = datetime.datetime.utcnow()
        self.hash_contents = []
        self.status = DownLoadInfoEnum.Unknown

    def save_commit(self):
        json_string = json.dumps(self.__dict__, default=__json_converter__)
        track_file_path = self.get_track_file_path()
        if not os.path.isdir(pathlib.Path(track_file_path).parent.__str__()):
            os.makedirs(pathlib.Path(track_file_path).parent.__str__(), exist_ok=True)
        with open(track_file_path, "wb") as fs:
            fs.write(json_string.encode('utf8'))
        self.status = DownLoadInfoEnum.Ready

    def get_modify_time_online(self) -> str:
        ret = os.path.getmtime(self.file_path)
        return datetime.datetime.fromtimestamp(ret).strftime("%Y-%m-%d %H:%M:%S")

    def get_track_file_path(self):
        return os.path.join(lib.config.get_app_track_dir(), self.id)

    def is_content_change(self):
        online_hash = self.get_hash_content_online()
        if len(self.hash_contents) != len(online_hash):
            return True
        for x in self.hash_contents:
            if x not in online_hash:
                return True
        return False

    def is_change(self):
        if self.status != DownLoadInfoEnum.Ready:
            return False
        if self.size_in_bytes != self.get_size_online():
            return True
        else:
            return set(self.hash_contents) != set(self.get_hash_content_online())

    def get_hash_content_online(self, step: int = 5):

        if os.path.getsize(self.file_path) == 0:
            return []
        ret_list = []
        hash_size_skip = int(math.floor(os.path.getsize(self.file_path) / step))
        hash_size = 1024
        with open(self.file_path, "rb") as f:
            bytes_read = f.read()
            ret = lib.data_hashing.hash_chunk(bytes_read)
            ret_list += [ret]
        return ret_list

    def get_hash_content_online_delete(self, step: int = 5):

        if os.path.getsize(self.file_path) == 0:
            return []
        ret_list = []
        hash_size_skip = int(math.floor(os.path.getsize(self.file_path) / step))
        hash_size = 1024
        with open(self.file_path, "rb") as f:
            bytes_read = f.read(hash_size)
            while len(bytes_read) > 0:
                skip_to = hash_size_skip + f.tell()
                f.seek(skip_to)
                if len(bytes_read) == 0:
                    return ret_list
                ret = lib.data_hashing.hash_chunk(bytes_read)
                ret_list += [ret]
                bytes_read = f.read(hash_size)
        return ret_list

    # def get_hash_first_online(self):

    #
    # def get_hash_last_online(self):
    #     last_chunk = __read_last_bytes__(self.file_path)
    #     ret = lib.data_hashing.hash_chunk(last_chunk)
    #     return ret

    def get_size_online(self):
        return os.path.getsize(self.file_path)

    def commit_change(self):
        self.size_in_bytes = self.get_size_online()
        self.hash_contents = self.get_hash_content_online()
        self.modify_time = self.get_modify_time_online()

    def do_download(self):
        is_existing = False
        if os.path.isfile(self.file_path):
            is_existing = True
            try:
                os.remove(self.file_path)
                is_existing = False
            except:
                pass
        if is_existing:
            self.commit_change()
            self.save_commit()
        else:
            response = requests.get(self.url, stream=True, verify=False)

            # Check for successful response
            if response.status_code == 200:
                with open(self.file_path, "wb") as f:

                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)

                self.commit_change()
                self.save_commit()
            else:
                response.raise_for_status()

            return None


__cache__ = {}


def get_info_by_url(url: str) -> DownLoadInfo:
    global __cache__
    info = config.get_app_config(url)
    return info


def get_info_by_id(id: str) -> DownLoadInfo:
    global __cache__
    if isinstance(__cache__.get(id), DownLoadInfo):
        return __cache__.get(id)
    ret = None
    is_load_from_log = False
    if os.path.isfile(os.path.join(lib.config.get_app_track_dir(), id)):
        try:
            with open(os.path.join(lib.config.get_app_track_dir(), id), "rb") as f:
                data = json.loads(f.read().decode("utf8"))
                ret = DownLoadInfo(data.get("url"))
                for k, v in data.items():
                    ret.__dict__[k] = v
                is_load_from_log = True
                # __cache__[id] = ret.__dict__
            if isinstance(ret, DownLoadInfo):
                ret.commit_change()
                if is_load_from_log:
                    ret.status = DownLoadInfoEnum.Ready
                __cache__[id] = ret
                return ret

        except:
            os.remove(os.path.join(lib.config.get_app_track_dir(), id))
