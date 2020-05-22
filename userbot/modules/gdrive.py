# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


import asyncio
import math
import os
import time
from pySmartDL import SmartDL
from telethon import events
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import ResumableUploadError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import file, client, tools
from userbot import (G_DRIVE_CLIENT_ID, G_DRIVE_CLIENT_SECRET,
                     G_DRIVE_AUTH_TOKEN_DATA, GDRIVE_FOLDER_ID, BOTLOG_CHATID,
                     TEMP_DOWNLOAD_DIRECTORY, CMD_HELP, LOGS)
from userbot.events import register
from mimetypes import guess_type
import httplib2
import subprocess
from userbot.modules.upload_download import progress, humanbytes, time_formatter

# Json dosyasının yolu, script ile aynı dizinde bulunmalıdır.
G_DRIVE_TOKEN_FILE = "./auth_token.txt"
# API konsolundan kişisel bilgilerinizi kopyalar
CLIENT_ID = G_DRIVE_CLIENT_ID
CLIENT_SECRET = G_DRIVE_CLIENT_SECRET
# Mevcut alan tüm alanları kontrol eder: https://developers.google.com/drive/scopes
OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.file"
# URI'yi yüklü uygulamalar için yönlendirir, olduğu gibi bırakılabilir.
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
# Yüklenecek klasör IDsini ayarlamaya yarayan evrensel değer
parent_id = GDRIVE_FOLDER_ID
# Dizinlerin mimeType değerini belirten evrensel değer
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"


@register(pattern=r"^.gdrive(?: |$)(.*)", outgoing=True)
async def gdrive_upload_function(dryb):
    """ .gdrive komutu dosyalarınızı Google Drive'a uploadlar. """
    await dryb.edit("İşleniyor ...")
    input_str = dryb.pattern_match.group(1)
    if CLIENT_ID is None or CLIENT_SECRET is None:
        return
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
        required_file_name = None
    if "|" in input_str:
        url, file_name = input_str.split("|")
        url = url.strip()
        # https://stackoverflow.com/a/761825/4723940
        file_name = file_name.strip()
        head, tail = os.path.split(file_name)
        if head:
            if not os.path.isdir(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head)):
                os.makedirs(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head))
                file_name = os.path.join(head, tail)
        downloaded_file_name = TEMP_DOWNLOAD_DIRECTORY + "" + file_name
        downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        display_message = None
        while not downloader.isFinished():
            status = downloader.get_status().capitalize()
            total_length = downloader.filesize if downloader.filesize else None
            downloaded = downloader.get_dl_size()
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed()
            elapsed_time = round(diff) * 1000
            progress_str = "[{0}{1}] {2}%".format(
                ''.join(["▰" for i in range(math.floor(percentage / 10))]),
                ''.join(["▱"
                         for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2))
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"{status}...\
                \nURL: {url}\
                \nDosya adı: {file_name}\
                \n{progress_str}\
                \n{humanbytes(downloaded)} of {humanbytes(total_length)}\
                \nBitiş: {estimated_total_time}"

                if round(diff %
                         10.00) == 0 and current_message != display_message:
                    await dryb.edit(current_message)
                    display_message = current_message
            except Exception as e:
                LOGS.info(str(e))
                pass
        if downloader.isSuccessful():
            await dryb.edit(
                "`{}` dizinine indirme başarılı. \nGoogle Drive'a yükleme başlatılıyor.."
                .format(downloaded_file_name))
            required_file_name = downloaded_file_name
        else:
            await dryb.edit("Geçersiz URL\n{}".format(url))
    elif input_str:
        input_str = input_str.strip()
        if os.path.exists(input_str):
            required_file_name = input_str
            await dryb.edit(
                "`{}` dosyası sunucuda bulundu. Google Drive'a yükleme başlatılıyor.."
                .format(input_str))
        else:
            await dryb.edit(
                "Sunucuda dosya bulunamadı. Lütfen doğru dosya konumunu belirtin.")
            return False
    elif dryb.reply_to_msg_id:
        try:
            c_time = time.time()
            downloaded_file_name = await dryb.client.download_media(
                await dryb.get_reply_message(),
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop(
                ).create_task(progress(d, t, dryb, c_time, "İndiriliyor...")))
        except Exception as e:
            await dryb.edit(str(e))
        else:
            required_file_name = downloaded_file_name
            await dryb.edit(
                "`{}` dizinine indirme başarrılı. \nGoogle Drive'a yükleme başlatılıyor.."
                .format(downloaded_file_name))
    if required_file_name:
        if G_DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(G_DRIVE_AUTH_TOKEN_DATA)
        # Token dosyasının olup olmadığını kontrol eder, eğer yoksa yetkilendirme kodu ile oluşturur.
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, dryb)
            http = authorize(G_DRIVE_TOKEN_FILE, storage)
        # Yetkilendirir, dosya parametrelerini edinir, dosyayı uploadlar ve URL'yi indirme için paylaşır.
        http = authorize(G_DRIVE_TOKEN_FILE, None)
        file_name, mime_type = file_ops(required_file_name)
        # required_file_name tam dosya yoluna sahiptir.
        # Bazen API başlangıç URI'sini geri alırken hatayla karşılaşır.
        try:
            g_drive_link = await upload_file(http, required_file_name,
                                             file_name, mime_type, dryb,
                                             parent_id)
            await dryb.edit(
                f"Dosya :`{required_file_name}`\nUpload başarılı! \nİndirme linki: [Google Drive]({g_drive_link})!"
            )
        except Exception as e:
            await dryb.edit(
                f"Google Drive'a yükleme başarısız.\nHata kodu:\n`{e}`")


@register(pattern=r"^.ggd(?: |$)(.*)", outgoing=True)
async def upload_dir_to_gdrive(event):
    await event.edit("İşleniyor ...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        return
    input_str = event.pattern_match.group(1)
    if os.path.isdir(input_str):
        # Yapılacaklar: Gereksiz kodlar kaldırılacak.
        if G_DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(G_DRIVE_AUTH_TOKEN_DATA)
        # Token dosyasının olup olmadığını kontrol eder, eğer yoksa yetkilendirme kodunu isteyerek oluşturur.
        storage = None
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
        http = authorize(G_DRIVE_TOKEN_FILE, storage)
        # Yetkilendirir, dosya parametrelerini edinir, dosyayı uploadlar ve URL'yi indirme için paylaşır.
        # Öncelikle alt dizin oluşturur.
        dir_id = await create_directory(
            http, os.path.basename(os.path.abspath(input_str)), parent_id)
        await DoTeskWithDir(http, input_str, event, dir_id)
        dir_link = "https://drive.google.com/folderview?id={}".format(dir_id)
        await event.edit(f"Google Drive bağlantın [burada]({dir_link})")
    else:
        await event.edit(f"{input_str} dizini bulunamadı.")


@register(pattern=r"^.list(?: |$)(.*)", outgoing=True)
async def gdrive_search_list(event):
    await event.edit("İşleniyor ...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        return
    input_str = event.pattern_match.group(1).strip()
    # Yapılacaklar: Gereksiz kodlar kaldırılacak.
    if G_DRIVE_AUTH_TOKEN_DATA is not None:
        with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
            t_file.write(G_DRIVE_AUTH_TOKEN_DATA)
    # Token dosyasının olup olmadığını kontrol eder, eğer yoksa yetkilendirme kodunu isteyerek oluşturur.
    storage = None
    if not os.path.isfile(G_DRIVE_TOKEN_FILE):
        storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
    http = authorize(G_DRIVE_TOKEN_FILE, storage)
    # Yetkilendirir, dosya parametrelerini edinir, dosyayı uploadlar ve URL'yi indirme için paylaşır.
    await event.edit(f"Google Drive'ınızda {input_str} aranıyor...")
    gsearch_results = await gdrive_search(http, input_str)
    await event.edit(gsearch_results, link_preview=False)


@register(
    pattern=
    r"^.gsetf https?://drive\.google\.com/drive/u/\d/folders/([-\w]{25,})",
    outgoing=True)
async def download(set):
    """ .gsetf komutu dizini belirtmenizi sağlar. """
    await set.edit("İşleniyor ...")
    input_str = set.pattern_match.group(1)
    if input_str:
        parent_id = input_str
        await set.edit(
            "Özel Klasör ID'si başarıyla ayarlandı. Sonraki uploadlar şuraya uploadlanacak: {parent_id} (`.gsetclear` komutunu vermediğiniz sürece)"
        )
        await set.delete()
    else:
        await set.edit(
            ".gdrivesp <GDrive Klasörü> komutuyla yeni dosyaların uploadlanacağı klasörü belirtebilirsiniz."
        )


@register(pattern="^.gsetclear$", outgoing=True)
async def download(gclr):
    """ .gsetclear komutu özel dizini kaldırmanıza yarar. """
    await gclr.reply("İşleniyor ...")
    parent_id = GDRIVE_FOLDER_ID
    await gclr.edit("Özel Klasör ID'si başarıyla temizlendi.")


@register(pattern="^.gfolder$", outgoing=True)
async def show_current_gdrove_folder(event):
    if parent_id:
        folder_link = f"https://drive.google.com/drive/folders/" + parent_id
        await event.edit(
            f"UserBot'um dosyaları [şuraya]({folder_link}) uploadlıyor.")
    else:
        await event.edit(
            f"UserBot'um dosyaları Google Drive'ın kök dizinine uploadlıyor.\
            \nUploadlanan dosyalar [burada](https://drive.google.com/drive/my-drive)"
        )


# Dosyanın tipini ve ismini çağırır
def file_ops(file_path):
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    file_name = file_path.split("/")[-1]
    return file_name, mime_type


async def create_token_file(token_file, event):
    # OAuth üzerinden kişisel bilgileri geri alır.
    flow = OAuth2WebServerFlow(CLIENT_ID,
                               CLIENT_SECRET,
                               OAUTH_SCOPE,
                               redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    async with event.client.conversation(BOTLOG_CHATID) as conv:
        await conv.send_message(
            f"Bu linke git ve kodu kopyalayıp yanıtla: {authorize_url}"
        )
        response = conv.wait_event(
            events.NewMessage(outgoing=True, chats=BOTLOG_CHATID))
        response = await response
        code = response.message.message.strip()
        credentials = flow.step2_exchange(code)
        storage = Storage(token_file)
        storage.put(credentials)
        return storage


def authorize(token_file, storage):
    # Kişisel bilgilei alır
    if storage is None:
        storage = Storage(token_file)
    credentials = storage.get()
    # httplib2.Http objesi oluşturur ve kişisel bilgilerinizle yetkilendirir.
    http = httplib2.Http()
    credentials.refresh(http)
    http = credentials.authorize(http)
    return http


async def upload_file(http, file_path, file_name, mime_type, event, parent_id):
    # Google Drive servis örneği oluşturur.
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    # Dosya tipi açıklaması
    media_body = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    body = {
        "title": file_name,
        "description": "Seden UserBot kullanılarak yüklendi.",
        "mimeType": mime_type,
    }
    if parent_id:
        body["parents"] = [{"id": parent_id}]
    # İzinlerin açıklaması: Linke sahip olan herkes görebilir.
    # Diğer izinler şurada bulunabilir: https://developers.google.com/drive/v2/reference/permissions
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True
    }
    # Dosyayı ekler
    file = drive_service.files().insert(body=body, media_body=media_body)
    response = None
    display_message = ""
    while response is None:
        status, response = file.next_chunk()
        await asyncio.sleep(1)
        if status:
            percentage = int(status.progress() * 100)
            progress_str = "[{0}{1}] {2}%".format(
                "".join(["▰" for i in range(math.floor(percentage / 10))]),
                "".join(["▱"
                         for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2))
            current_message = f"Google Drive'a uploadlanıyor.\nDosya Adı: {file_name}\n{progress_str}"
            if display_message != current_message:
                try:
                    await event.edit(current_message)
                    display_message = current_message
                except Exception as e:
                    LOGS.info(str(e))
                    pass
    file_id = response.get("id")
    # Yeni izinleri ekler.
    drive_service.permissions().insert(fileId=file_id,
                                       body=permissions).execute()
    # Dosya örneğini tanımlar ve indirmek için bağlantıyı edinir.
    file = drive_service.files().get(fileId=file_id).execute()
    download_url = file.get("webContentLink")
    return download_url


async def create_directory(http, directory_name, parent_id):
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True
    }
    file_metadata = {
        "title": directory_name,
        "mimeType": G_DRIVE_DIR_MIME_TYPE
    }
    if parent_id:
        file_metadata["parents"] = [{"id": parent_id}]
    file = drive_service.files().insert(body=file_metadata).execute()
    file_id = file.get("id")
    drive_service.permissions().insert(fileId=file_id,
                                       body=permissions).execute()
    LOGS.info("Created Gdrive Folder:\nName: {}\nID: {} ".format(
        file.get("title"), file_id))
    return file_id


async def DoTeskWithDir(http, input_directory, event, parent_id):
    list_dirs = os.listdir(input_directory)
    if len(list_dirs) == 0:
        return parent_id
    r_p_id = None
    for a_c_f_name in list_dirs:
        current_file_name = os.path.join(input_directory, a_c_f_name)
        if os.path.isdir(current_file_name):
            current_dir_id = await create_directory(http, a_c_f_name,
                                                    parent_id)
            r_p_id = await DoTeskWithDir(http, current_file_name, event,
                                         current_dir_id)
        else:
            file_name, mime_type = file_ops(current_file_name)
            # current_file_name tam dosya dizinine sahiptir.
            g_drive_link = await upload_file(http, current_file_name,
                                             file_name, mime_type, event,
                                             parent_id)
            r_p_id = parent_id
    # Yapılacaklar: Burada bir bug var :(
    return r_p_id


async def gdrive_list_file_md(service, file_id):
    try:
        file = service.files().get(fileId=file_id).execute()
        # LOGS.info(dosya)
        file_meta_data = {}
        file_meta_data["title"] = file["title"]
        mimeType = file["mimeType"]
        file_meta_data["createdDate"] = file["createdDate"]
        if mimeType == G_DRIVE_DIR_MIME_TYPE:
            # bir klasör ise
            file_meta_data["mimeType"] = "directory"
            file_meta_data["previewURL"] = file["alternateLink"]
        else:
            # bir dosya ise
            file_meta_data["mimeType"] = file["mimeType"]
            file_meta_data["md5Checksum"] = file["md5Checksum"]
            file_meta_data["fileSize"] = str(humanbytes(int(file["fileSize"])))
            file_meta_data["quotaBytesUsed"] = str(
                humanbytes(int(file["quotaBytesUsed"])))
            file_meta_data["previewURL"] = file["downloadUrl"]
        return json.dumps(file_meta_data, sort_keys=True, indent=4)
    except Exception as e:
        return str(e)


async def gdrive_search(http, search_query):
    if parent_id:
        query = "'{}' in parents and (title contains '{}')".format(
            parent_id, search_query)
    else:
        query = "title contains '{}'".format(search_query)
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    page_token = None
    res = ""
    while True:
        try:
            response = drive_service.files().list(
                q=query,
                spaces="drive",
                fields="nextPageToken, items(id, title, mimeType)",
                pageToken=page_token).execute()
            for file in response.get("items", []):
                file_title = file.get("title")
                file_id = file.get("id")
                if file.get("mimeType") == G_DRIVE_DIR_MIME_TYPE:
                    res += f"`[FOLDER] {file_title}`\nhttps://drive.google.com/drive/folders/{file_id}\n\n"
                else:
                    res += f"`{file_title}`\nhttps://drive.google.com/uc?id={file_id}&export=download\n\n"
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
        except Exception as e:
            res += str(e)
            break
    msg = f"**Google Drive Araması**:\n`{search_query}`\n\n**Sonuçlar**\n\n{res}"
    return msg


CMD_HELP.update({
    "gdrive":
    ".gdrive <dosya yolu / yanıtlayarak / URL|dosya-adı>\
    \nKullanım: Belirtilen dosyayı Google Drive'a uploadlar.\
    \n\n.gsetf <GDrive Klasör URL'si>\
    \nKullanım: Yeni dosyaların upladlanacağı klasörü belirler.\
    \n\n.gsetclear\
    \nKullanım: Varsayılan upload dizinine geri döndürür.\
    \n\n.gfolder\
    \nKullanım: Halihazırda kullanılan upload dizinini gösterir.\
    \n\n.list <sorgu>\
    \nKullanım: Google Drive'da bulunan dosyalar ve dizinlerde arama yapar.\
    \n\n.ggd <sunucudaki-klasör-yolu>\
    \nKullanım: Belirtilen dizindeki tüm dosyaları Google Drive'a uploadlar."
})
