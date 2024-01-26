import uuid

import jwt

import lib.contents, lib.config, lib.errors
import lib.ui
import logging
import lib.extension_mapping
# from lib.watch_file import do_watch_file
import lib.contents
import lib.ui_controller
import json

keys_check = {
    'tenant',
    'resourceId',
    'checkOutUrl',
    'checkOutMethod',
    'checkOutHeader',
    'checkOutData',
    'checkInUrl',
    'checkInMethod',
    'checkInHeader',
    'checkInData',
    'accessToken',
    'resourceExt'
}


def check_data(data: dict):
    data_keys = set(list(data.keys()))
    miss_fields = list(keys_check.difference(data_keys))
    if len(miss_fields) > 0:
        error_message = "These info are missing in you data:" + "\n".join(miss_fields)
        return dict(
            error_code="MissingField",
            error_message=error_message,
            fields=list(keys_check.difference(data_keys)),

        )
    else:
        access_token = data["accessToken"]
        resource_id = data["resourceId"]
        resource_ext = data["resourceExt"]
        check_out_url = data["checkOutUrl"]

        check_out_method = data["checkOutMethod"]
        check_out_header = data["checkOutHeader"]
        check_out_data = data["checkOutData"]
        check_in_url = data["checkInUrl"]
        check_in_method = data["checkInMethod"]
        check_in_header = data["checkInHeader"]
        check_in_data = data["checkInData"]
        tenant = data["tenant"]
        if check_out_method not in ["get", "post", "put", "patch", "delete"]:
            return dict(
                error_code="Invalidvalue",
                error_message="checkOutMethod mus be 'post' , 'get','put','patch' or 'delete'"
            )
        if check_in_method not in ["get", "post", "put", "patch", "delete"]:
            return dict(
                error_code="Invalidvalue",
                error_message="checkInMethod mus be 'post' , 'get','put','patch' or 'delete'"
            )
        header = None
        try:
            header = jwt.get_unverified_header(access_token)
        except:
            return dict(
                error_code="InvalidToken",
                error_message="Can not verify Token header"
            )
        try:
            algorithm = header['alg']
            decoded_payload = jwt.decode(access_token, options={"verify_signature": False})
            return dict(
                tenant=tenant,
                access_token=access_token,
                resource_id=resource_id,
                resource_ext=resource_ext,
                check_in_url=check_in_url,
                check_in_method=check_in_method,
                check_out_url=check_out_url,
                check_out_method=check_out_method,
                access_token_payload=decoded_payload,
                client_mac_adress="{:012X}".format(uuid.getnode()),
                check_out_data= check_out_data,
                check_out_header= check_out_header,
                check_in_data= check_in_data,
                check_in_header= check_in_header
            )
        except:
            return dict(
                error_code="InvalidToke",
                error_message="Can not read Token"
            )


async def send_to_client(websocket, data):
    await websocket.send(json.dumps(data))


async def send_error_to_client(websocket, error_code, error_message):
    error_data = dict(
        error_code=error_code,
        error_message=error_message
    )
    await websocket.send(json.dumps(error_data))

import requests.exceptions
async def resolve_async(websocket, client_data: dict) -> lib.contents.DownLoadInfo:
    try:
        doc_info = lib.contents.get_info_by_url(client_data)

        if doc_info is None:
            return None

        if doc_info is None:
            return
        assert isinstance(doc_info, lib.contents.DownLoadInfo)
        await send_to_client(websocket,
                             dict(message="Loading..",
                                  id=doc_info.id)
                             )
        if doc_info.file_ext in lib.extension_mapping.word_extensions:

            if doc_info.do_download():
                lib.ui_controller.loader.load_word(doc_info.file_path)
                return doc_info
        elif doc_info.file_ext in lib.extension_mapping.powerpoint_extensions:
            if doc_info.do_download():
                lib.ui_controller.loader.load_power_point(doc_info.file_path)
                return doc_info
        elif doc_info.file_ext in lib.extension_mapping.excel_extensions:
            if doc_info.do_download():
                lib.ui_controller.loader.load_excel(doc_info.file_path)
                return doc_info
        elif doc_info.file_ext in lib.extension_mapping.notepad_extensions:
            if doc_info.do_download():
                lib.ui_controller.loader.load_note_pad(doc_info.file_path)
                return doc_info
        elif doc_info.file_ext in lib.extension_mapping.paint_extensions:
            if doc_info.do_download():
                lib.ui_controller.loader.load_paint_app(doc_info.file_path)
                return doc_info
        else:
            lib.ui_controller.loader.show_message_error("The file type might not be supported.")
            await send_to_client(websocket,
                                 dict(
                                     message="The file type might not be supported.",
                                     id=doc_info.id,
                                     error="UnsupportedType")
                                 )

    except lib.errors.Error as e:
        lib.ui_controller.loader.show_message_error(e.message)
        await send_to_client(
            websocket,
            dict(
                message="The file type might not be supported.",
                id=doc_info.id,
                error="UnsupportedType"
            ))
    except requests.exceptions.ConnectionError:
        lib.ui_controller.loader.show_message_error(f"Can not connect to {doc_info.check_out_url}")
        await send_to_client(
            websocket,
            dict(
                message=f"Can not connect to {doc_info.check_out_url}",
                id=doc_info.id,
                error="ConnectFail"
            ))
    # except Exception as e:
    #     logging.error(e)
    #     raise e
