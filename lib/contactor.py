import os
import time
import lib.config
import requests
import requests.exceptions
import lib.loggers


# def __do_upload__(app_name, upload_id, src_path, info: lib.config.UploadInfo):
#     import lib.contents
#     data = lib.contents.get_info_by_id(id=upload_id)
#     assert isinstance(data,lib.contents.DownLoadInfo)
#     data.do_upload()
#
#     # /lvfile/api/{app_name}/files/update_source/{id}
#     # if info.port:
#     #     url_update_content = f"{info.scheme}://{info.host}:{info.port}/lvfile/api/{app_name}/files/update_source/{upload_id}"
#     # else:
#     #     url_update_content = f"{info.scheme}://{info.host}/lvfile/api/{app_name}/files/update_source/{upload_id}"
#     info.is_in_upload = True
#     files = {"content": open(src_path, "rb")}  # Replace with your file path
#     response = requests.post(url_update_content, files=files)
#     response.raise_for_status()
#     info.is_in_upload = False
#
#     lib.loggers.logger.info(f"{src_path} was sync to {url_update_content}")
#     return response


def do_upload(app_name, upload_id, src_path, info: lib.config.UploadInfo):
    import lib.contents
    data = lib.contents.get_info_by_id(id=upload_id)
    assert isinstance(data, lib.contents.DownLoadInfo)
    ret = data.do_upload()
    return ret
