import win32com.client

import lib.contents, lib.config, lib.errors
import lib.ui
import logging
import lib.extension_mapping
# from lib.watch_file import do_watch_file
import lib.contents


async def resolve_async(websocket, request_path, url_file,
                        upload_info: lib.config.UploadInfo) -> lib.contents.DownLoadInfo:
    try:
        doc_info = lib.contents.download(url_file)
        if doc_info is None:
            return None
        if doc_info is None:
            return

        if doc_info.file_ext in lib.extension_mapping.word_extensions:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = True  # Make Word window visible
            doc = word.Documents.Open(doc_info.file_path)
            word.Activate()  # This brings Word to the foreground
            doc_info.start_watch()

            return doc_info
        elif doc_info.file_ext in lib.extension_mapping.powerpoint_extensions:
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            powerpoint.Visible = True  # Make Word window visible
            doc = presentation = powerpoint.Presentations.Open(doc_info.file_path)
            powerpoint.Activate()  # This brings Word to the foreground
            doc_info.start_watch()
            return doc_info
        elif doc_info.file_ext in lib.extension_mapping.excel_extensions:
            excel = win32com.client.Dispatch("Excel.Application")
            workbook = excel.Workbooks.Open(doc_info.file_path)
            excel.Visible = True
            workbook.Activate()
            doc_info.start_watch()
            return doc_info


        elif doc_info.file_ext in lib.extension_mapping.notepad_extensions:
            import subprocess
            subprocess.Popen(["notepad", doc_info.file_path])
            doc_info.start_watch()
        elif doc_info.file_ext in lib.extension_mapping.paint_extensions:
            import subprocess
            subprocess.Popen(["MSPaint", doc_info.file_path])
            doc_info.start_watch()
            return doc_info
        else:
            raise lib.errors.Error("This file does not support")
    except lib.errors.Error as e:
        lib.ui.show_message_error(e.message)
    # except Exception as e:
    #     logging.error(e)
