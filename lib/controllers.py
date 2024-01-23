

import lib.contents, lib.config, lib.errors
import lib.ui
import logging
import lib.extension_mapping
# from lib.watch_file import do_watch_file
import lib.contents
import lib.ui_controller

async def resolve_async(websocket, request_path, url_file,
                        upload_info: lib.config.UploadInfo) -> lib.contents.DownLoadInfo:
    try:
        doc_info = lib.contents.get_info_by_url(url_file)


        if doc_info is None:
            return None

        if doc_info is None:
            return
        assert isinstance(doc_info,lib.contents.DownLoadInfo)
        doc_info.do_download()
        if doc_info.file_ext in lib.extension_mapping.word_extensions:
            lib.ui_controller.loader.load_word(doc_info.file_path)
            return doc_info
        elif doc_info.file_ext in lib.extension_mapping.powerpoint_extensions:
            lib.ui_controller.loader.load_power_point(doc_info.file_path)

            return doc_info
        elif doc_info.file_ext in lib.extension_mapping.excel_extensions:
            lib.ui_controller.loader.load_excel(doc_info.file_path)

            return doc_info


        elif doc_info.file_ext in lib.extension_mapping.notepad_extensions:
            lib.ui_controller.loader.load_note_pad(doc_info.file_path)

        elif doc_info.file_ext in lib.extension_mapping.paint_extensions:
            lib.ui_controller.loader.load_paint_app(doc_info.file_path)

            return doc_info
        else:
            raise lib.errors.Error("This file does not support")
    except lib.errors.Error as e:
        lib.ui.show_message_error(e.message)
    # except Exception as e:
    #     logging.error(e)
