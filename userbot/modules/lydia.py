# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

# credit goes to @snapdragon and @devpatel_73 for making it work on this userbot.
#

from userbot.events import register
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot import LYDIA_API_KEY
import coffeehouse
from time import time
import io
import coffeehouse as cf
from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
import asyncio
from telethon import events
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


try:
    from userbot.modules.sql_helper.lydia_sql import get_s, get_all_s, add_s, remove_s
except:
    logging.log(level=logging.WARNING,
                msg="Lydia veritabanı bağlantısı başarısız oldu")

# SQL dışı mod
ACC_LYDIA = {}

if LYDIA_API_KEY:
    api_key = LYDIA_API_KEY
    api_client = API(api_key)
    lydia = LydiaAI(api_client)


@register(outgoing=True, pattern="^.repcf$")
async def repcf(event):
    if event.fwd_from:
        return
    await event.edit("İşleniyor...")
    try:
        session = lydia.create_session()
        reply = await event.get_reply_message()
        msg = reply.text
        text_rep = session.think_thought(msg)
        await event.edit("**Lydia diyor ki**: {0}".format(text_rep))
    except Exception as e:
        await event.edit(str(e))

@register(outgoing=True, pattern="^.addcf$")
async def addcf(event):
    if event.fwd_from:
        return
    await event.edit("Şimdilik SQL dışı modda çalışıyor...")
    await asyncio.sleep(3)
    await event.edit("İşleniyor...")
    reply_msg = await event.get_reply_message()
    if reply_msg:
        session = lydia.create_session()
        session_id = session.id
        if reply_msg.from_id is None:
            return await event.edit("Geçersiz kullanıcı türü.")
        ACC_LYDIA.update({(event.chat_id & reply_msg.from_id): session})
        await event.edit("Lydia, {} kullanıcısı için {} sohbetinde başarıyla etkinleştirildi!".format(str(reply_msg.from_id), str(event.chat_id)))
    else:
        await event.edit("Lydia AI'yı etkinleştirmek için bir kullanıcıyı yanıtlayın")

@register(outgoing=True, pattern="^.remcf$")
async def remcf(event):
    if event.fwd_from:
        return
    await event.edit("Şimdilik SQL dışı modda çalışıyor...")
    await asyncio.sleep(3)
    await event.edit("İşleniyor...")
    reply_msg = await event.get_reply_message()
    try:
        del ACC_LYDIA[event.chat_id & reply_msg.from_id]
        await event.edit("Lydia, {} kullanıcısı için {} sohbetinde başarıyla devre dışı bırakıldı!".format(str(reply_msg.from_id), str(event.chat_id)))
    except Exception:
        await event.edit("Bu kullanıcıda Lydia aktif değil.")


@register(incoming=True, disable_edited=True)
async def user(event):
    user_text = event.text
    try:
        session = ACC_LYDIA[event.chat_id & event.from_id]
        msg = event.text
        async with event.client.action(event.chat_id, "typing"):
            text_rep = session.think_thought(msg)
            wait_time = 0
            for i in range(len(text_rep)):
                wait_time = wait_time + 0.1
            await asyncio.sleep(wait_time)
            await event.reply(text_rep)
    except (KeyError, TypeError):
        return

CMD_HELP.update({
    "lydia":
    ".addcf <kullanıcı adı/yanıtlayarak>\
\nKullanım: Lydia'nın otomatik sohbetini etkinleştirir. \
\n\n.remcf <kullanıcı adı/yanıtlayarak>\
\nKullanım: Lydia'nın otomatik sohbetini devre dışı bırakır. \
\n\n.repcf <kullanıcı adı/yanıtlayarak>\
\nKullanım: Lydia'nın otomatik sohbetiini belli bir kişi için etkinleştirir."
})
