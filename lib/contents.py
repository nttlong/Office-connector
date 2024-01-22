import datetime
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
catch_watch_dir = os.path.join(config.app_dir, "logs")

try:
    os.makedirs(catch_watch_dir, exist_ok=True)
except Exception as e:
    lib.loggers.logger.error(e)
def __json_converter__(obj):
  if isinstance(obj, datetime.datetime):
    return obj.isoformat()
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

class DownLoadInfo:
    hash_first: str
    hash_last: str
    file_path: str
    app_name: str
    upload_id: str
    file_name_only: str
    file_ext: str
    scheme: str
    host: str
    port: str
    is_in_upload: bool
    is_in_download: bool
    created_on: datetime.datetime
    size_in_bytes:int
    is_ready:bool
    is_sync: bool

    def __init__(self):
        self.hash_first = None
        self.hash_last = None
        self.file_path = None
        self.app_name = None
        self.upload_id = None
        self.file_name_only = None
        self.file_ext = None
        self.scheme = None
        self.host = None
        self.port = None
        self.is_in_upload = False
        self.is_in_download = False
        self.created_on = datetime.datetime.utcnow()
        self.size_in_bytes=0
        self.is_ready=False
        self.is_sync = False

    def start_watch(self):
        pass

    def __del__(self):
        global __cache__
        del __cache__[self.upload_id]

    @property
    def id(self):
        """Getter for the `value` property."""
        return self.upload_id

    @id.setter
    def id(self, new_value):
        """Setter for the `value` property."""
        global __cache__

        self.upload_id = new_value
        __cache__[self.upload_id] = self.__dict__
        json_string = json.dumps( self.__dict__, default=__json_converter__)
        track_file_path = self.get_track_file_path()
        if not os.path.isdir(pathlib.Path(track_file_path).parent.__str__()):
            os.makedirs(pathlib.Path(track_file_path).parent.__str__(),exist_ok=True)
        with open(track_file_path,"wb") as fs:
            fs.write(json_string.encode('utf8'))

    def get_track_file_path(self):
        global catch_watch_dir
        return os.path.join(catch_watch_dir,self.upload_id)

    def is_change(self):
        if not self.is_ready:
            return False
        if self.size_in_bytes != self.get_size_online():
            return True
        else:
            online_hash_first = self.get_hash_first_online()
            if online_hash_first!=self.hash_first:
                return True
            else:
                online_hash_last= self.get_hash_last_online()
                return online_hash_last!=self.hash_last



    def get_hash_first_online(self):
        with open(self.file_path,"rb") as f:
            first_1024_bytes = f.read(1024)
            ret= lib.data_hashing.hash_chunk(first_1024_bytes)
            return ret

    def get_hash_last_online(self):
        last_chunk = __read_last_bytes__(self.file_path)
        ret = lib.data_hashing.hash_chunk(last_chunk)
        return ret

    def get_size_online(self):
        return os.path.getsize(self.file_path)

    def commit(self):
        self.size_in_bytes=self.get_size_online()
        self.hash_first= self.get_hash_first_online()
        self.hash_last = self.get_hash_last_online()
        self.id=self.upload_id


def get_info_by_id(id:str)->DownLoadInfo:
    global  __cache__
    ret= DownLoadInfo()
    if __cache__.get(id) is None:
        if os.path.isfile(os.path.join(catch_watch_dir,id)):
            try:
                with open(os.path.join(catch_watch_dir,id),"rb") as f:
                    data = json.loads(f.read().decode("utf8"))
                    for k,v in data.items():
                        ret.__dict__[k] = v
                    __cache__[id] = ret.__dict__
                    ret.is_ready=True
                    return ret

            except:
                os.remove(os.path.join(catch_watch_dir,id))

    else:
        data = __cache__.get(id)
        for k, v in data.items():
            ret.__dict__[k] = v
        ret.is_ready = True
        return ret


def download(url) -> typing.Optional[DownLoadInfo]:
    ret = DownLoadInfo()
    info = config.get_app_config(url)
    download_dir = os.path.join(config.app_data_dir, info.app_name)
    os.makedirs(download_dir, exist_ok=True)
    file_name = info.upload_id
    download_path = os.path.join(download_dir, f"{file_name}.{info.file_ext}")
    file_id = pathlib.Path(download_path).stem

    ret.is_in_download = False
    ret.port = info.port
    ret.scheme = info.scheme
    ret.file_ext = info.file_ext
    ret.app_name = info.app_name
    ret.file_name_only = info.file_name_only
    ret.file_path = download_path
    ret.host = info.host

    try:
        if os.path.isfile(download_path):
            os.remove(download_path)
    except:

        ret.commit()
        ret.id = info.upload_id
        return ret
    lib.cacher_tracking.downloading[file_id] = download_path
    ret.is_in_download = True
    response = requests.get(url, stream=True, verify=False)

    # Check for successful response
    if response.status_code == 200:
        size=0
        with open(download_path, "wb") as f:

            for chunk in response.iter_content(chunk_size=1024):
                if ret.hash_first is None:
                    ret.hash_first = lib.data_hashing.hash_chunk(chunk)
                if len(chunk)==1024:
                    last_chunk = chunk
                f.write(chunk)
                size+=len(chunk)


        ret.file_path = download_path
        ret.is_in_download = False

        ret.size_in_bytes= ret.get_size_online()
        last_chunk = __read_last_bytes__(download_path)
        ret.hash_last = lib.data_hashing.hash_chunk(last_chunk)
        ret.id = info.upload_id
        ret.is_ready = True
        return ret
    else:
        response.raise_for_status()

    return None
