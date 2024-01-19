import os
import pathlib
import uuid

import urllib3
app_data_dir= os.path.join(os.environ.get("USERPROFILE"),"AppData","Roaming","codx")
os.makedirs(app_data_dir,exist_ok=True)
import lib.errors

class UploadInfo:
    app_name:str
    upload_id:str
    file_name_only:str
    file_ext:str


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
        return ret_info
    except ValueError as e:
        raise lib.errors.Error("Invalid Codx server")
    except Exception as e:
        raise lib.errors.Error(type(e).__name__)