import lib.config
import requests
def do_upload(app_name, upload_id, src_path, info:lib.config.UploadInfo):
    if info.port:
        url_update_content = f"{info.scheme}://{info.host}:{info.port}/lvfile/api/files/update_source"
    else:
        url_update_content = f"{info.scheme}://{info.host}/lvfile/api/files/update_source"
    info.is_in_upload=True
    files = {"file": open(src_path, "rb")}  # Replace with your file path
    response = requests.post(url_update_content, files=files)
    info.is_in_upload=False