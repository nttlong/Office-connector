import os
import pathlib
import uuid
import traceback
import lib.loggers
import urllib3
app_data_dir= os.path.join(os.environ.get("USERPROFILE"),"AppData","Roaming","codx")
try:
    app_data_dir= os.path.join(os.path.expanduser("~\\AppData\\Local"),"Codx-Desktop-Connector")
    os.makedirs(app_data_dir,exist_ok=True)
    lib.loggers.logger.info(f"{app_data_dir} was create")

except Exception as e:
    lib.loggers.logger.error(e)
os.makedirs(app_data_dir,exist_ok=True)
import lib.errors

class UploadInfo:
    app_name:str
    upload_id:str
    file_name_only:str
    file_ext:str
    scheme:str
    host:str
    port:str
    is_in_upload:bool


def get_app_config(url:str)->UploadInfo:
    try:
        ret= urllib3.util.url.parse_url(url)
        app_name_pos_start = ret.path.index("/api/")+len("/api/")
        app_name_pos_end = ret.path.index("/",app_name_pos_start)
        app_name = ret.path[app_name_pos_start:app_name_pos_end]
        start_id_pos =ret.path.index("/",app_name_pos_end+1)+1
        end_id_pos = ret.path.index("/", start_id_pos + 1)
        id= ret.path[start_id_pos:end_id_pos]
        check_id= uuid.UUID(id)
        ret_info= UploadInfo()
        ret_info.app_name=app_name
        ret_info.upload_id=id
        file_name_only = pathlib.Path(ret.path).stem
        file_ext = pathlib.Path(ret.path).suffix
        if file_ext is None or file_ext=="":
            raise lib.errors.Error("Invalid file")
        else:
            file_ext=file_ext[1:]
        ret_info.file_ext=file_ext.lower()
        ret_info.file_name_only=file_name_only
        ret_info.scheme = ret.scheme
        ret_info.host = ret.host
        if ret.port:
            ret_info.port = str(ret.port)
        else:
            ret_info.port = None
        ret_info.is_in_upload=False

        return ret_info
    except ValueError as e:
        raise lib.errors.Error("Invalid Codx server")
    except Exception as e:
        raise lib.errors.Error(type(e).__name__)