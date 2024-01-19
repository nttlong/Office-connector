import win32com.client

import lib.contents, lib.config, lib.errors
import lib.ui
import logging
import lib.extension_mapping
from lib.watch_file import do_watch_file
logging.basicConfig(filename="my_app.log", level=logging.ERROR)
async def resolve_async(websocket, request_path, url_file,upload_info:lib.config.UploadInfo):
    try:
        doc_path = lib.contents.download(url_file)

        # app_key = lib.extension_mapping.app_word_mapping_dict.get(upload_info.file_ext)
        if upload_info.file_ext in lib.extension_mapping.word_extensions:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = True  # Make Word window visible
            doc = word.Documents.Open(doc_path)
            word.Activate()  # This brings Word to the foreground

            return doc_path
        elif upload_info.file_ext in lib.extension_mapping.powerpoint_extensions:
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            powerpoint.Visible = True  # Make Word window visible
            doc = presentation = powerpoint.Presentations.Open(doc_path)
            powerpoint.Activate()  # This brings Word to the foreground
            return doc_path
        elif upload_info.file_ext in lib.extension_mapping.excel_extensions:
            excel = win32com.client.Dispatch("Excel.Application")
            workbook = excel.Workbooks.Open(doc_path)
            excel.Visible = True
            workbook.Activate()
            return  doc_path


        elif upload_info.file_ext in lib.extension_mapping.notepad_extensions:
            import subprocess
            subprocess.Popen(["notepad",doc_path])
        elif upload_info.file_ext in lib.extension_mapping.paint_extensions:
            import subprocess
            subprocess.Popen(["MSPaint",doc_path])
            return doc_path
        else:
            raise lib.errors.Error("This file does not support")
    except lib.errors.Error as e:
        lib.ui.show_message_error(e.message)
    # except Exception as e:
    #     logging.error(e)


