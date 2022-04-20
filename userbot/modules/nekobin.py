# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Nekobin ile etkileşim için komutlar içeren UserBot modülü (https://nekobin.com/) """

import os
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.cmdhelp import CmdHelp
import aiohttp
import asyncio
import json

URL = "https://nekobin.com/"

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("dogbin")

# ████████████████████████████████ #

@register(outgoing=True, pattern=r"^.paste(?: |$)([\s\S]*)")
async def paste(pstl):
    """ .paste komutu metni doğrudan nekobine yapıştırır """

    match = pstl.pattern_match.group(1).strip()
    reply_id = pstl.reply_to_msg_id

    if not match and not reply_id:
        await pstl.edit(LANG['ELON_SAYS'])
        return

    if match:
        message = match
    elif reply_id:
        message = (await pstl.get_reply_message())
        if message.media:
            downloaded_file_name = await pstl.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r"
            os.remove(downloaded_file_name)
        else:
            message = message.message

    # Throwbin
    await pstl.edit(LANG['PASTING'])
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get("https://open-apis-rest.up.railway.app/api/nekobin?text=" + message) as response:

            html = await response.text()
            html2 = json.loads(html)
            if html2["status"] == "OK":
                reply_text = LANG['PASTED'] + "\n\n" + LANG['URL'] + " " + html2["data"]["url"]
                await pstl.edit(reply_text)
                if BOTLOG:
                    await pstl.client.send_message(
                        BOTLOG_CHATID,
                        f"Nekobine metin yapıştırma başarıyla yürütüldü",
                    )
            else:
                return await pstl.edit("__Sunucu ile ilgili bir sorun var. Daha sonra tekrar deneyin.__")


@register(outgoing=True, pattern="^.getpaste ?(.*)")
async def get_dogbin_content(event):
    """ .getpaste komutu Nekobin url içeriğini aktarır """
    url = event.pattern_match.group(1)

    if "nekobin" not in url:
        return await event.edit(LANG["UNSUPPORTED_URL"])
    
    await event.edit(LANG['DATA_CHECKING'])
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get("https://open-apis-rest.up.railway.app/api/nekobinget?url=" + url) as response:

            html = await response.text()
            html2 = json.loads(html)
            if html2["status"] == "OK":
                await event.edit(LANG["DOGBIN_DATA"] + "\n\n" + html2["data"])
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        LANG['DOGBIN_ENDED'],
                    )
            else:
                return await event.edit(LANG["DOGBIN_NOT_RESPOND"])

CmdHelp('paste').add_command(
    'paste', '<metin/yanıtlama>', 'Nekobin kullanarak yapıştırılmış veya kısaltılmış url oluşturma (https://nekobin.com)'
).add_command(
    'getpaste', "nekobin url", 'Nekobin url içeriğini metne aktarır (https://nekobin.com)'
).add()