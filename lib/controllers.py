import win32com.client

import lib.contents, lib.config, lib.errors
import lib.ui
import logging

logging.basicConfig(filename="my_app.log", level=logging.ERROR)
async def resolve_async(websocket, request_path, url_file,upload_info:lib.config.UploadInfo):
    try:
        doc_path = lib.contents.download(url_file)
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = True  # Make Word window visible
        doc = word.Documents.Open(doc_path)
        word.Activate()  # This brings Word to the foreground
        return doc_path
    except lib.errors.Error as e:
        lib.ui.show_message_error(e.message)
    except Exception as e:
        logging.error(e)


