import os
import uuid

import requests

from lib import config

def download(url):
    response = requests.get(url,verify=False)
    download_path= os.path.join(config.app_data_dir,str(uuid.uuid4()))
    with open(download_path, "wb") as f:
        f.write(response.content)
    return download_path