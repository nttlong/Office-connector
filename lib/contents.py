import datetime
import os
import pathlib
import uuid

import requests

from lib import config
import lib.cacher_tracking


def download(url):
    info = config.get_app_config(url)
    download_dir = os.path.join(config.app_data_dir, info.app_name)
    os.makedirs(download_dir, exist_ok=True)
    file_name = info.upload_id
    download_path = os.path.join(download_dir, file_name)
    file_id=pathlib.Path(download_path).stem

    try:
        if os.path.isfile(download_path):
            os.remove(download_path)
    except:
        return download_path
    lib.cacher_tracking.downloading[file_id] = download_path
    response = requests.get(url, verify=False)
    with open(download_path, "wb") as f:
        f.write(response.content)
    return download_path
