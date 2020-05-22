# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


import asyncio
import time
import threading
from asyncio import wait, sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.tspam")
async def tmeme(e):
    message = e.text
    messageSplit = message.split(" ", 1)
    tspam = str(messageSplit[1])
    message = tspam.replace(" ", "")
    for letter in message:
        await e.respond(letter)
    await e.delete()
    if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID,
                "#TSPAM \n\n"
                "TSpam başarıyla gerçekleştirildi"
                )

@register(outgoing=True, pattern="^.spam")
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        messageSplit = message.split(" ", 2)
        counter = int(messageSplit[1])
        spam_message = str(messageSplit[2])
        await asyncio.wait([e.respond(spam_message) for i in range(counter)])
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID,
                "#SPAM \n\n"
                "Spam başarıyla gerçekleştirildi"
                )
                               
@register(outgoing=True, pattern="^.bigspam")
async def bigspam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        messageSplit = message.split(" ", 2)
        counter = int(messageSplit[1])
        spam_message = str(messageSplit[2])
        for i in range(1, counter):
            await e.respond(spam_message)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID,
                "#BIGSPAM \n\n"
                "Bigspam başarıyla gerçekleştirildi"
                )
        
        
@register(outgoing=True, pattern="^.picspam")
async def tiny_pic_spam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        text = message.split()
        counter = int(text[1])
        link = str(text[2])
        for i in range(1, counter):
            await e.client.send_file(e.chat_id, link)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID,
                "#PICSPAM \n\n"
                "PicSpam başarıyla gerçekleştirildi"
                )


@register(outgoing=True, pattern="^.delayspam")
async def delayspammer(e):
    # Teşekkürler @ReversedPosix
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        messageSplit= message.split(" ", 3)
        spam_delay = float(messageSplit[1])
        counter = int(messageSplit[2])
        spam_message = str(messageSplit[3])
        from userbot.events import register
        await e.delete()
        delaySpamEvent = threading.Event()
        for i in range(1, counter):
            await e.respond(spam_message)
            delaySpamEvent.wait(spam_delay)
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID,
                "#DelaySPAM \n\n"
                "DelaySpam başarıyla gerçekleştirildi"
                )
                               
CMD_HELP.update({
    "spammer": ".tspam <metin>\
\nKullanım: Verilen mesajı tek tek göndererek spam yapar\
\n\n.spam <miktar> <metin>\
\nKullanım: Verilen miktarda spam gönderir\
\n\n.bigspam <miktar> <metin>\
\nKullanım: .spam komutunun büyük hali\
\n\n.picspam <miktar> <link>\
\nKullanım: Verilen miktarda resimli spam gönderir\
\n\n.delayspam <gecikme> <miktar> <metin>\
\nKullanım: Verilen miktar ve verilen gecikme ile gecikmeli spam yapar\
\n\n\nNOT : Sorumluluk size aittir!!"
})

