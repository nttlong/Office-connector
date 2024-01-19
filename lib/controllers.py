import win32com.client

import lib.contents


async def resolve_async(websocket, request_path, url_file):
    doc_path = lib.contents.download(url_file)
    word = win32com.client.Dispatch("Word.Application")

    word.Visible = True  # Make Word window visible

    doc = word.Documents.Open(doc_path)
    word.Activate()  # This brings Word to the foreground
    return doc_path