# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Dogbin ile etkileşim için komutlar içeren UserBot modülü(https://del.dog)"""

from requests import get, post, exceptions
import os
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.cmdhelp import CmdHelp
import aiohttp
import asyncio


URL = "https://throwbin.in/"

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("dogbin")

# ████████████████████████████████ #

@register(outgoing=True, pattern=r"^.paste(?: |$)([\s\S]*)")
async def paste(pstl):
    """ .paste komutu metni doğrudan throwbine yapıştırır """

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
    async with aiohttp.ClientSession() as client:
        html = await fetch(client)
        token = html.split('name="_token" value="')[1].split('"')[0]
        html2 = await poster(client, token, message)
        final_url = html2.split('<ClientResponse(')[1].split(')')[0]
        reply_text = (f"{LANG['PASTED']}\n\n"
            f"`{LANG['URL']}` {final_url}"
        )
        await pstl.edit(reply_text)
        if BOTLOG:
            await pstl.client.send_message(
                BOTLOG_CHATID,
                f"Throwbine metin yapıştırma başarıyla yürütüldü",
            )

@register(outgoing=True, pattern="^.getpaste ?(.*)")
async def get_dogbin_content(event):
    """ .getpaste komutu Throwbin url içeriğini aktarır """
    url = event.pattern_match.group(1)

    if "throwbin" not in url:
        return await event.edit(LANG["UNSUPPORTED_URL"])
    
    await event.edit(LANG['DATA_CHECKING'])
    async with aiohttp.ClientSession() as client:
        try:
            paste = await ıcerık_al(client, url) 
        except:
            return await event.edit(LANG["DOGBIN_NOT_RESPOND"])

        await event.edit(LANG["DOGBIN_DATA"] + "\n\n" + paste)
        if BOTLOG:
            await dog_url.client.send_message(
                BOTLOG_CHATID,
                LANG['DOGBIN_ENDED'],
            )



async def poster(client, token, text):
    async with client.post("https://throwbin.in/create", json={"_token": str(token), "title": "AsenaUserBot", "syntax": "text/x-textile", "content": str(text)}) as resp2:
        return str(resp2)

async def fetch(client):
    async with client.get('https://throwbin.in/') as resp:
        assert resp.status == 200
        return await resp.text()

async def ıcerık_al(client, url):
    async with client.get(url) as resp:
        assert resp.status == 200
        txt = await resp.text()
        return txt.split('<pre><code>')[1].split('</code></pre>')[0]

CmdHelp('paste').add_command(
    'paste', '<metin/yanıtlama>', 'Throwbin kullanarak yapıştırılmış veya kısaltılmış url oluşturma (https://throwbin.in)'
).add_command(
    'getpaste', None, 'Throwbin url içeriğini metne aktarır (https://throwbin.in)'
).add()