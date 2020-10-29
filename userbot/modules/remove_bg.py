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
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("remove_bg")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.rbg(?: |$)(.*)")
async def kbg(remob):
    """ .rbg komutu ile görüntünün arka planını kaldırın """
    if REM_BG_API_KEY is None:
        await remob.edit(
            LANG['NEED_API_KEY']
        )
        return
    input_str = remob.pattern_match.group(1)
    message_id = remob.message.id
    if remob.reply_to_msg_id:
        message_id = remob.reply_to_msg_id
        reply_message = await remob.get_reply_message()
        await remob.edit(LANG['TRYING'])
        try:
            if isinstance(
                    reply_message.media, MessageMediaPhoto
            ) or "image" in reply_message.media.document.mime_type.split('/'):
                downloaded_file_name = await remob.client.download_media(
                    reply_message, TEMP_DOWNLOAD_DIRECTORY)
                await remob.edit(LANG['RBG'])
                output_file_name = await ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
            else:
                await remob.edit(LANG['CANT_RBG'])
        except Exception as e:
            await remob.edit(str(e))
            return
    elif input_str:
        await remob.edit(
            f"`{LANG['ONLINE_RBG']}`\n{input_str}")
        output_file_name = await ReTrieveURL(input_str)
    else:
        await remob.edit(LANG['NEED'])
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "removed_bg.png"
            await remob.client.send_file(
                remob.chat_id,
                remove_bg_image,
                caption=LANG['CAPTION'],
                force_document=True,
                reply_to=message_id)
            await remob.delete()
    else:
        await remob.edit("**Hata {}**\n`{}`".format(LANG['ERROR'],
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

CmdHelp('rgb').add_command(
    'rbg', '<Resim bağlantısı/yanıt>', 'remove.bg API kullanarak görüntülerin arka planını kaldırır.'
).add()