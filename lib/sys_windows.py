import time

import lib.sys_abtraction
import os
from pathlib import Path
import psutil
import os
class SysOs(lib.sys_abtraction.BaseSys):
    def get_list_of_files(self,app_data_dir):
        import os
        ret = os.walk(app_data_dir)
        ret_list = list(ret)
        if len(ret_list)==0:
            return []
        root,sub_dirs,_ = ret_list[0]

        ret_data = []
        for x in sub_dirs:
            root_sub,_,ret_files = list(os.walk(os.path.join(root,x)))[0]
            ret_data+=[ os.path.join(root_sub,f) for f in ret_files]

        return ret_data

    def is_file_in_use(self,file_path):
        for proc in psutil.process_iter():
            try:
                open_files = proc.open_files()
                for path, fname in open_files:

                    if os.path.samefile(path, file_path):
                        return True  # File is accessed by a process
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass  # Ignore potential errors
            time.sleep(0.001)
        return False  # File is not accessed

    def delete_file(self, file_path):
            try:
                os.remove(file_path)
            except:
                pass

