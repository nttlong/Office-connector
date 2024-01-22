import os
import time
import lib.config
import requests
import requests.exceptions
import lib.loggers
def __do_upload__(app_name, upload_id, src_path, info:lib.config.UploadInfo):
    # /lvfile/api/{app_name}/files/update_source/{id}
    if info.port:
        url_update_content = f"{info.scheme}://{info.host}:{info.port}/lvfile/api/{app_name}/files/update_source/{upload_id}"
    else:
        url_update_content = f"{info.scheme}://{info.host}/lvfile/api/{app_name}/files/update_source/{upload_id}"
    info.is_in_upload = True
    files = {"content": open(src_path, "rb")}  # Replace with your file path
    response = requests.post(url_update_content, files=files)
    info.is_in_upload = False

    lib.loggers.logger.info(f"{src_path} was sync to {url_update_content}")
    return response
def do_upload(app_name, upload_id, src_path, info:lib.config.UploadInfo):
    count=10
    while count>0:
        try:
            res = __do_upload__(app_name, upload_id, src_path, info)
            count =0

        except requests.exceptions.ConnectionError as e:
            lib.loggers.logger.error(e)
            count -=1
            time.sleep(2)
        except PermissionError as e:
            lib.loggers.logger.error(e)
            count -= 1
            time.sleep(2)
        except Exception as e:
            lib.loggers.logger.error(e)
            info.is_in_upload=False