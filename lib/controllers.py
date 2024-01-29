import pathlib
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
    # 'tenant',
    # 'resourceId',
    'source.url',
    'deste'
}
from urllib.parse import urlparse

def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)
src_error= dict(
            error_code="MissingField",
            error_message="'src' was not found ('src' must be an object with url of content source). Example {\n"
                          "'src':'url:'http://...'\n"
                          "'method':'get'// one of value in [get,post,delete,put, patch]. Default value is 'post'},"
                          "'header':{put your header here if if url in 'src' require header} \n"
                          "'data':{put your data here if if url in 'src' require data \n"
                          "}" ,
            fields=["src.url"],

        )
dst_error= dict(
            error_code="MissingField",
            error_message="'dst' was not found ('dst' must be an object with url of content source). Example {\n"
                          "'dst':'url:'http://...'\n"
                          "'method':'get'// one of value in [get,post,delete,put, patch]}. Default value is 'post'"
                          "'header':{put your header here if if url in 'dst' require header} \n"
                          "'data':{put your data here if if url in 'dst' require data \n"
                          "}",
            fields=["dst.url"],

        )
def check_data(data: dict):
    import lib.data_hashing
    if not isinstance(data.get('src'),dict):
        return src_error
    if not isinstance(data.get('dst'),dict):
        return dst_error

    src = data.get('src') or {}
    dst = data.get('dst') or {}
    if src.get('url') is None or not isinstance(src["url"],str) or not is_valid_url(src["url"]):
        return src_error
    if dst.get('url') is None or not isinstance(dst["url"],str) or not is_valid_url(dst["url"]):
        return dst_error


    else:
        # access_token = data["accessToken"]
        hash_id = lib.data_hashing.has_dict(data)
        resource_id =  hash_id
        resource_ext = data.get("resourceExt")
        if resource_ext is None:
            resource_ext = pathlib.Path(urlparse(src["url"]).path).suffix
            if resource_ext and isinstance(resource_ext,str):
                resource_ext=resource_ext[1:]
            else:
                return dict(
                    error_code= "MissingField",
                    error_message = "The application can not inspect extension of file in url. Please set 'resourceExt'",
                    fields=["resourceExt"]

                )

        check_out_url = src.get("url")

        check_out_method = src.get("method") or "post"
        check_out_header = src.get("header")
        check_out_data = src.get("data")
        check_in_url = dst.get("url")
        check_in_method = dst.get("method") or "post"
        check_in_header = dst.get("header")
        check_in_data = dst.get("data")
        # tenant = data["tenant"]
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
        # try:
        #     header = jwt.get_unverified_header(access_token)
        # except:
        #     return dict(
        #         error_code="InvalidToken",
        #         error_message="Can not verify Token header"
        #     )
        try:
            # algorithm = header['alg']
            # decoded_payload = jwt.decode(access_token, options={"verify_signature": False})
            ret_dict= dict(

                # access_token={},
                resource_id=resource_id,
                resource_ext=resource_ext,
                check_in_url=check_in_url,
                check_in_method=check_in_method,
                check_out_url=check_out_url,
                check_out_method=check_out_method,
                # access_token_payload=decoded_payload,
                client_mac_adress="{:012X}".format(uuid.getnode()),
                check_out_data= check_out_data,
                check_out_header= check_out_header,
                check_in_data= check_in_data,
                check_in_header= check_in_header
            )
            return ret_dict
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
