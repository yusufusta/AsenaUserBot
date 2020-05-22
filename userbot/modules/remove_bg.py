# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

# Prakasaka tarafından portlanmıştır.
#

import io
import os
import requests
from userbot.events import register
from telethon.tl.types import MessageMediaPhoto
from userbot import CMD_HELP, REM_BG_API_KEY, TEMP_DOWNLOAD_DIRECTORY


@register(outgoing=True, pattern="^.rbg(?: |$)(.*)")
async def kbg(remob):
    """ .rbg komutu ile görüntünün arka planını kaldırın """
    if REM_BG_API_KEY is None:
        await remob.edit(
            "`Hata: Remove.BG API key eksik! Lütfen ekleyin.`"
        )
        return
    input_str = remob.pattern_match.group(1)
    message_id = remob.message.id
    if remob.reply_to_msg_id:
        message_id = remob.reply_to_msg_id
        reply_message = await remob.get_reply_message()
        await remob.edit("`İşleniyor..`")
        try:
            if isinstance(
                    reply_message.media, MessageMediaPhoto
            ) or "image" in reply_message.media.document.mime_type.split('/'):
                downloaded_file_name = await remob.client.download_media(
                    reply_message, TEMP_DOWNLOAD_DIRECTORY)
                await remob.edit("`Bu görüntüden arka plan kaldırılıyor..`")
                output_file_name = await ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
            else:
                await remob.edit("`Bunun arka planını nasıl kaldırabilirim ?`"
                                 )
        except Exception as e:
            await remob.edit(str(e))
            return
    elif input_str:
        await remob.edit(
            f"`Çevrimiçi görüntüden arka planı kaldırma`\n{input_str}")
        output_file_name = await ReTrieveURL(input_str)
    else:
        await remob.edit("`Arka planı kaldırmak için bir şeye ihtiyacım var.`")
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "removed_bg.png"
            await remob.client.send_file(
                remob.chat_id,
                remove_bg_image,
                caption="Remove.bg kullanılarak arka plan kaldırıldı",
                force_document=True,
                reply_to=message_id)
            await remob.delete()
    else:
        await remob.edit("**Hata (Geçersiz API key olduğunu tamhin ediyorum..)**\n`{}`".format(
            output_file_name.content.decode("UTF-8")))


async def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post("https://api.remove.bg/v1.0/removebg",
                      headers=headers,
                      files=files,
                      allow_redirects=True,
                      stream=True)
    return r


async def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    data = {"image_url": input_url}
    r = requests.post("https://api.remove.bg/v1.0/removebg",
                      headers=headers,
                      data=data,
                      allow_redirects=True,
                      stream=True)
    return r


CMD_HELP.update({
    "rbg":
    ".rbg <Resim bağlantısı> veya herhangi bir görüntüye cevap verin (Uyarı: çıkartmalar üzerinde çalışmaz.)\
\nKullanım: remove.bg API kullanarak görüntülerin arka planını kaldırır."
})
