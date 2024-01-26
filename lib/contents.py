import datetime
import enum
import math
import os
import pathlib
import time
import typing
import uuid

import requests
import lib.data_hashing
from lib import config, ui
import lib.cacher_tracking
import lib.loggers
import json

__cache__ = {}


def get_app_name():
    return "Codx DMS desktop connector"


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
    created_on: datetime.datetime
    size_in_bytes: int
    is_ready: bool
    is_sync: bool
    modify_time: typing.Optional[datetime.datetime]
    hash_contents: typing.Optional[typing.List[str]]
    check_out_url: str
    check_out_method: str
    check_out_header: dict
    check_out_data: dict
    check_in_url: str
    check_in_method: str
    check_in_header: dict
    check_in_data: dict
    size_in_bytes: int
    modify_time: str
    url: str
    id: str
    status: DownLoadInfoEnum
    client_data:dict
    host:str
    port:str

    def __init__(self, data: dict):
        self.client_data = data["client_data"]
        if not isinstance(data,dict):
            print("error")
        assert isinstance(self.client_data, dict)
        self.url = self.client_data["check_out_url"]
        self.download_dir = os.path.join(config.app_data_dir, self.client_data["tenant"])
        file_name = self.client_data["resource_id"]
        file_ext = self.client_data["resource_ext"].lower()
        os.makedirs(self.download_dir, exist_ok=True)



        self.is_in_download = False
        self.check_out_url = self.client_data["check_out_url"]
        self.check_out_method = self.client_data["check_out_method"]
        self.check_out_data = self.client_data["check_out_data"]
        self.check_out_header = self.client_data["check_out_header"]
        self.file_ext = file_ext
        self.app_name = self.client_data["tenant"]
        self.file_name_only = file_name
        self.check_in_url = self.client_data["check_in_url"]
        self.check_in_method = self.client_data["check_in_method"]
        self.check_in_header = self.client_data["check_in_header"]
        self.check_in_data = self.client_data["check_in_data"]
        self.created_on = datetime.datetime.utcnow()
        self.hash_contents = []
        self.status = DownLoadInfoEnum.Unknown
        import urllib3.util
        info = urllib3.util.parse_url(self.check_out_url)


        self.host = info.host
        self.port = "_"+str((info.port or "80"))
        self.file_path = os.path.join(self.download_dir,self.host.replace(".","_")+self.port, f"{file_name}")
        os.makedirs(pathlib.Path(self.file_path ).parent.__str__(),exist_ok=True)
        self.id = pathlib.Path(self.file_path).stem

    def get_meta(self):
        ret_etxt = os.getxattr(self.file_path, "user.metadata")
        return ret_etxt

    def save_meta(self):
        json_string = json.dumps(self.__dict__, default=__json_converter__)
        os.setxattr(self.file_path, "codx.metadata", json_string)

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

        ret = os.path.join(lib.config.get_app_track_dir(),self.app_name,self.host.replace(".","_")+self.port, self.id)
        os.makedirs(pathlib.Path(ret).parent.__str__(), exist_ok=True)
        return ret

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
            ret = set(self.hash_contents) != set(self.get_hash_content_online())
            if ret:
                return True
        return False

    def get_hash_content_online(self, step: int = 3):

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

    def get_size_online(self):
        return os.path.getsize(self.file_path)

    def commit_change(self):
        self.size_in_bytes = self.get_size_online()
        self.hash_contents = self.get_hash_content_online()
        self.modify_time = self.get_modify_time_online()

    def do_download(self):
        import lib.ui_controller
        is_existing = False
        self.is_ready = False
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
            self.is_ready = True
            return True
        else:
            lib.ui_controller.loader.show_message(f"Check out content")

            response = self.init_request_and_get_response(
                url=self.check_out_url,
                file_path=None,
                medthod=self.check_out_method,
                data=self.check_out_data,
                header=self.check_out_header,
                hash_to_server="",
                hash_len=lib.config.hash_len()
            )
            lib.ui_controller.loader.show_message(f"Check out content is complete and saving file ...")
            if response.status_code == 200:
                try:
                    with open(self.file_path, "wb") as f:

                        for chunk in response.iter_content(chunk_size=1024):
                            f.write(chunk)

                    self.commit_change()
                    self.save_commit()
                    lib.ui_controller.loader.show_message(f"Saving file is Ok")
                    self.is_ready = True
                    return True
                except Exception as e:

                    lib.ui_controller.loader.show_message_error(f"Can not get content from {self.check_out_url}")
                    lib.loggers.logger.debug(e)
                    return False
            elif response.status_code == 401:
                lib.ui_controller.loader.show_message_error(f"Can not download {self.check_out_url}, Authenticate fail")
                lib.loggers.logger.error(response.content.decode("utf8"))
                return False
            else:
                lib.ui_controller.loader.show_message_error(f"Can not download {self.check_out_url}")
                lib.loggers.logger.error(response.content.decode("utf8"))
                return False
            return False

    def do_upload(self):
        import lib.ui_controller
        self.is_ready = False
        lib.ui_controller.loader.show_message(f"Check in content ...")
        count=10
        is_ok = False
        while count>0:
            try:
                hash_to_server =".".join(self.get_hash_content_online(step=lib.config.hash_len()))
                response = self.init_request_and_get_response(
                    url=self.check_in_url,
                    medthod=self.check_in_method,
                    header=self.check_in_header,
                    data=self.check_in_data,
                    file_path=self.file_path,
                    hash_to_server= hash_to_server,
                    hash_len=lib.config.hash_len()
                )
                response.raise_for_status()
                count=0
                is_ok= True
                ret_txt = response.content.decode("utf8")
                try:
                    ret_data = json.loads(ret_txt)
                    return ret_data
                except:
                    return ret_txt
            except:
                time.sleep(2)
                lib.ui_controller.loader.show_message(f"Check in content ...(re-try: {9-count})")
                count-=1

        if not is_ok:
            lib.ui_controller.loader.show_message_error(f"can not check in ({self.check_in_url})")

        return  None
    def init_request_and_get_response(self, url, medthod, header, data, file_path,hash_to_server,hash_len):

        web_method = getattr(requests, medthod)
        _header_ = {
            "mac_address_id": "{:012X}".format(uuid.getnode()),
            "hash_contents": hash_to_server,
            "hash_len":str(hash_len)
        }
        if data and file_path is None:
            _header_ = {**_header_, **{'Content-Type': 'application/json'}}
        if header:
            header = {**_header_, **header}
        if not file_path:
            response = web_method(
                url=url,
                json=data,
                headers=header,
                stream=True,
                verify=False
            )
            return response
        else:
            files = {"content": open(file_path, "rb")}
            response = web_method(
                url=url,
                data=data,
                headers=header,
                stream=True,
                verify=False,
                files=files
            )
            return response


__cache__ = {}


def get_info_by_url(client_data: dict) -> DownLoadInfo:
    global __cache__
    return get_info_by_id(client_data=client_data)


def get_info_by_id(id: typing.Optional[str] = None, client_data: typing.Optional[dict] = None,track_file:typing.Optional[str]=None) -> DownLoadInfo:
    try:
        global __cache__
        id = id
        if isinstance(client_data, dict):
            id = client_data["resource_id"]

        if isinstance(track_file,str) and  isinstance(__cache__.get(track_file), DownLoadInfo):
            return __cache__.get(track_file)
        ret = None
        is_load_from_log = False
        if isinstance(track_file,str) and os.path.isfile(track_file):
            def run():
                with open(track_file, "rb") as f:
                    data = json.loads(f.read().decode("utf8"))
                    ret = DownLoadInfo(data)
                    for k, v in data.items():
                        ret.__dict__[k] = v
                    is_load_from_log = True
                    # __cache__[id] = ret.__dict__
                    if isinstance(ret, DownLoadInfo):
                        ret.commit_change()
                        if is_load_from_log:
                            ret.status = DownLoadInfoEnum.Ready
                        __cache__[track_file] = ret
                        return ret

                return None

            ret= run()
            if ret:
                return ret
            else:
                os.remove(os.path.join(lib.config.get_app_track_dir(), id))
                return None


        elif client_data:
            ret = DownLoadInfo(dict(client_data=client_data))
            return ret

    except FileNotFoundError:
        if client_data:
            ret = DownLoadInfo(dict(client_data=client_data))
            return ret