# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Sunucuya dosya indirme/yükleme yapmayı sağlayan UserBot modülüdür. """

import json
import os
import zipfile
import subprocess
import time
import math
import re

from pySmartDL import SmartDL
import asyncio
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo

from userbot import LOGS, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, BOT_USERNAME
from userbot.events import register

def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Upload-download için genel process_callback dir."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}] {2}%\n".format(
            ''.join(["▰" for i in range(math.floor(percentage / 10))]),
            ''.join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        if file_name:
            await event.edit("{}\nDosya Adı: `{}`\n{}".format(
                type_of_ps, file_name, tmp))
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))


def humanbytes(size):
    """ Boyut okunabilir olması için bayt olarak gösterilir """
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """ Daha güzel görünmesi için zamanı milisaniye olarak belirtir. """
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " gün, ") if days else "") + \
        ((str(hours) + " saat, ") if hours else "") + \
        ((str(minutes) + " dakika, ") if minutes else "") + \
        ((str(seconds) + " saniye, ") if seconds else "") + \
        ((str(milliseconds) + " milisaniye, ") if milliseconds else "")
    return tmp[:-2]


@register(pattern=r".download(?: |$)(.*)", outgoing=True)
async def download(target_file):
    """ .download komutu userbot sunucusuna dosya indirmenizi sağlar. """
    await target_file.edit("İşleniyor...")
    input_str = target_file.pattern_match.group(1)
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
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
            progress_str = "[{0}{1}] {2}%".format(
                ''.join(["▰" for i in range(math.floor(percentage / 10))]),
                ''.join(["▱"
                         for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2))
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"{status}..\
                \nBağlantı: {url}\
                \nDosya adı: {file_name}\
                \n{progress_str}\
                \n{humanbytes(downloaded)} of {humanbytes(total_length)}\
                \nTahmini bitiş: {estimated_total_time}"

                if round(diff %
                         10.00) == 0 and current_message != display_message:
                    await target_file.edit(current_message)
                    display_message = current_message
            except Exception as e:
                LOGS.info(str(e))
        if downloader.isSuccessful():
            await target_file.edit("`{}` konumuna indirme başarılı.".format(
                downloaded_file_name))
        else:
            await target_file.edit("Geçersiz bağlantı\n{}".format(url))
    elif target_file.reply_to_msg_id:
        try:
            c_time = time.time()
            downloaded_file_name = await target_file.client.download_media(
                await target_file.get_reply_message(),
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop(
                ).create_task(
                    progress(d, t, target_file, c_time, "İndiriliyor...")))
        except Exception as e:  # pylint:disable=C0103,W0703
            await target_file.edit(str(e))
        else:
            await target_file.edit("`{}` konumuna indirme başarılı.".format(
                downloaded_file_name))
    else:
        await target_file.edit(
            "Sunucuma indirmek için bir mesajı yanıtlayın.")


@register(pattern=r".uploadir (.*)", outgoing=True)
async def uploadir(udir_event):
    """ .uploadir komutu bir klasördeki tüm dosyaları uploadlamanıza yarar """
    input_str = udir_event.pattern_match.group(1)
    if os.path.exists(input_str):
        await udir_event.edit("İşleniyor...")
        lst_of_files = []
        for r, d, f in os.walk(input_str):
            for file in f:
                lst_of_files.append(os.path.join(r, file))
            for file in d:
                lst_of_files.append(os.path.join(r, file))
        LOGS.info(lst_of_files)
        uploaded = 0
        await udir_event.edit(
            " {} dosya bulundu. Upload birazdan başlayacak. Lütfen bekleyin :)".format(
                len(lst_of_files)))
        for single_file in lst_of_files:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                c_time = time.time()
                if not caption_rts.lower().endswith(".mp4"):
                    await udir_event.client.send_file(
                        udir_event.chat_id,
                        single_file,
                        caption=caption_rts,
                        force_document=False,
                        allow_cache=False,
                        reply_to=udir_event.message.id,
                        progress_callback=lambda d, t: asyncio.get_event_loop(
                        ).create_task(
                            progress(d, t, udir_event, c_time, "Uploadlanıyor...",
                                     single_file)))
                else:
                    thumb_image = os.path.join(input_str, "thumb.jpg")
                    c_time = time.time()
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    await udir_event.client.send_file(
                        udir_event.chat_id,
                        single_file,
                        caption=caption_rts,
                        thumb=thumb_image,
                        force_document=False,
                        allow_cache=False,
                        reply_to=udir_event.message.id,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                                round_message=False,
                                supports_streaming=True,
                            )
                        ],
                        progress_callback=lambda d, t: asyncio.get_event_loop(
                        ).create_task(
                            progress(d, t, udir_event, c_time, "Uploadlanıyor...",
                                     single_file)))
                os.remove(single_file)
                uploaded = uploaded + 1
        await udir_event.edit(
            "{} dosya başarıyla uploadlandı.".format(uploaded))
    else:
        await udir_event.edit("404: Directory Not Found")


@register(pattern=r".upload (.*)", outgoing=True)
async def upload(u_event):
    """ .upload komutu userbot sunucusundan dosya uploadlamaya yarar. """
    await u_event.edit("İşleniyor...")
    input_str = u_event.pattern_match.group(1)
    if input_str in ("userbot.session", "config.env"):
        await u_event.edit("`Bu tehlikeli bir operasyon! Onaylanmadı!`")
        return
    if os.path.exists(input_str):
        c_time = time.time()
        await u_event.client.send_file(
            u_event.chat_id,
            input_str,
            force_document=True,
            allow_cache=False,
            reply_to=u_event.message.id,
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, u_event, c_time, "Uploadlanıyor...", input_str)))
        await u_event.edit("Upload başarılı !!")
    else:
        await u_event.edit("404: Dosya bulunamadı")

@register(pattern=r".unzip", outgoing=True)  
async def zip(event):
    if event.fwd_from:
        return
    mone = await event.edit("Dosya indiriliyor...")
    extracted = TEMP_DOWNLOAD_DIRECTORY + "extracted/"
    thumb_image_path = TEMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
    if not os.path.isdir(extracted):
        os.makedirs(extracted)
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = time.time()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "`İndiriliyor...`")
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = time.time()
            ms = end - start
            await mone.edit("`{}, {} saniyede indirildi.`".format(downloaded_file_name, ms))

        with zipfile.ZipFile(downloaded_file_name, 'r') as zip_ref:
            zip_ref.extractall(extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        #filename = filename + "/"
        await event.edit("`İndirme başarılı! Dosya Zipten Çıkarılıyor!`")
        # r=root, d=directories, f = files
        for single_file in filename:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                force_document = False
                supports_streaming = True
                document_attributes = []
                if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True
                        )
                    ]
                
                await event.client.send_file(
                    event.chat_id,
                    single_file,
                    caption=f"`{caption_rts}`",
                    force_document=force_document,
                    supports_streaming=supports_streaming,
                    allow_cache=False,
                    reply_to=event.message.id,
                    attributes=document_attributes,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, event, c_time, "trying to upload")
                    )
                )
                os.remove(single_file)
        os.remove(downloaded_file_name)
    else:
        await event.edit("`Lütfen bir Zip'e yanıt verin!`")


@register(pattern="^.wupload ?(.+?|) (.*)")
async def wupload(event):
    await event.edit("`Dosya indiriliyor...`")
    PROCESS_RUN_TIME = 100
    input_str = event.pattern_match.group(1)
    selected_transfer = event.pattern_match.group(2)
    bas = time.time()
    if input_str:
        file_name = input_str
    else:
        HOST = ["anonfiles", "transfer", "filebin", "tmpninja", "anonymousfiles", "megaupload", "bayfiles", "tempsh", "letsupload"]
        if selected_transfer in HOST:
            reply = await event.get_reply_message()
            file_name = await event.client.download_media(
                reply.media,
                TEMP_DOWNLOAD_DIRECTORY
            )
        else:
            await event.edit("`Belirtilen host bulunamadı! Bulunan hostlar: anonfiles|transfer|filebin|tmpninja|anonymousfiles|megaupload|bayfiles|letsupload|vshare`")
            return
    await event.edit("`Dosya indirme işlemi başarılı. Yükleniyor...`")
    CMD_WEB = {
        "anonfiles": "curl -F \"file=@{full_file_path}\" https://anonfiles.com/api/upload",
        "transfer": "curl --upload-file \"{full_file_path}\" https://transfer.sh/{bare_local_name}",
        "tmpninja": "curl -F file=@\"{full_file_path}\" https://tmp.ninja/api.php?d=upload-tool",
        "filebin": "curl -X POST --data-binary \"@{full_file_path}\" -H \"filename: {bare_local_name}\" \"https://filebin.net\"",
        "anonymousfiles": "curl -F file=\"@{full_file_path}\" https://api.anonymousfiles.io/",
        "megaupload": "curl -F \"file=@{full_file_path}\" https://megaupload.is/api/upload",
        "tempsh": "curl -T \"{full_file_path}\" https://temp.sh",
        "bayfiles": "curl -F \"file=@{full_file_path}\" https://bayfiles.com/api/upload",
        "letsupload": "curl -F \"file=@{full_file_path}\" https://api.letsupload.cc/upload",
        "vshare": "curl -F \"file=@{full_file_path}\" https://api.vshare.is/upload"
    }
    filename = os.path.basename(file_name)
    try:
        selected_one = CMD_WEB[selected_transfer].format(
            full_file_path=file_name,
                        bare_local_name=filename
        )
    except KeyError:
        await event.edit("`Bilinmeyen host sitesi. Yüklenebilir siteler: ` anonfiles|transfer|filebin|tmpninja|anonymousfiles|megaupload|bayfiles|letsupload|vshare")
        return
    cmd = selected_one
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()

    zaman = time.time() - bas
    await event.edit("`Başarılı bir şekilde yüklendi. Link alınıyor...`")
    if t_response:
        try:
            t_response = json.dumps(json.loads(t_response), sort_keys=True, indent=4)
        except Exception as e:
            pass
        
        try:
            urll = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", t_response)[0]
        except:
            urll = t_response
            await event.edit(urll)
            return
        if BOT_USERNAME != None:
            results = await event.client.inline_query(
                BOT_USERNAME,
                f"{urll} {zaman} {selected_transfer}"
            )
            await results[0].click(
                event.chat_id,
                reply_to=event.reply_to_msg_id,
                hide_via=True
            )
            await event.delete()
        else:
            await event.edit(urll)

def get_video_thumb(file, output=None, width=90):
    """ Video kapak resmini gösterir """
    metadata = extractMetadata(createParser(file))
    popen = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file,
            "-ss",
            str(
                int((0, metadata.get("duration").seconds
                     )[metadata.has("duration")] / 2)),
            "-filter:v",
            "scale={}:-1".format(width),
            "-vframes",
            "1",
            output,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if not popen.returncode and os.path.lexists(file):
        return output
    return None


def extract_w_h(file):
    """ Bir medyanın yüksekliğini-genişliğini gösterir. """
    command_to_run = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file,
    ]
    # https://stackoverflow.com/a/11236144/4723940
    try:
        t_response = subprocess.check_output(command_to_run,
                                             stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        LOGS.warning(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


@register(pattern=r".uploadas(stream|vn|all) (.*)", outgoing=True)
async def uploadas(uas_event):
    """ .uploadas komutu size upload yaparken bazı argümanlar belirtmenizi sağlar. """
    await uas_event.edit("Lütfen bekleyin...")
    type_of_upload = uas_event.pattern_match.group(1)
    supports_streaming = False
    round_message = False
    spam_big_messages = False
    if type_of_upload == "stream":
        supports_streaming = True
    if type_of_upload == "vn":
        round_message = True
    if type_of_upload == "all":
        spam_big_messages = True
    input_str = uas_event.pattern_match.group(2)
    thumb = None
    file_name = None
    if "|" in input_str:
        file_name, thumb = input_str.split("|")
        file_name = file_name.strip()
        thumb = thumb.strip()
    else:
        file_name = input_str
        thumb_path = "a_random_f_file_name" + ".jpg"
        thumb = get_video_thumb(file_name, output=thumb_path)
    if os.path.exists(file_name):
        metadata = extractMetadata(createParser(file_name))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        try:
            if supports_streaming:
                c_time = time.time()
                await uas_event.client.send_file(
                    uas_event.chat_id,
                    file_name,
                    thumb=thumb,
                    caption=input_str,
                    force_document=False,
                    allow_cache=False,
                    reply_to=uas_event.message.id,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop(
                    ).create_task(
                        progress(d, t, uas_event, c_time, "Uploadlanıyor...",
                                 file_name)))
            elif round_message:
                c_time = time.time()
                await uas_event.client.send_file(
                    uas_event.chat_id,
                    file_name,
                    thumb=thumb,
                    allow_cache=False,
                    reply_to=uas_event.message.id,
                    video_note=True,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=0,
                            w=1,
                            h=1,
                            round_message=True,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop(
                    ).create_task(
                        progress(d, t, uas_event, c_time, "Uploadlanıyor...",
                                 file_name)))
            elif spam_big_messages:
                await uas_event.edit("TBD: Halihazırda uygulanamadı.")
                return
            os.remove(thumb)
            await uas_event.edit("Upload başarılı !!")
        except FileNotFoundError as err:
            await uas_event.edit(str(err))
    else:
        await uas_event.edit("404: Dosya bulunamadı.")


CMD_HELP.update({
    "download":
    ".download <bağlantı-dosya adı> (ya da bir şeye cevap vererek)\
\nKullanım: Sunucuya dosyayı indirir.\
\n\n.upload <sunucudaki dosya yolu>\
\nKullanım: Sunucunuzdaki bir dosyayı sohbete upload eder.",
})
CMD_HELP["wupload"] = "Kullanım: <dosyaya yanıt verin> anonfiles|transfer|filebin|tmpninja|anonymousfiles|megaupload|bayfiles|letsupload|vshare"
