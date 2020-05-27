# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

# @NaytSeyd tarafından portlanmıştır.
# @frknkrc44 tarafından düzenlenmiştir.

import asyncio
import json
import logging

import requests
from userbot import CMD_HELP
from userbot.events import register

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


@register(outgoing=True, pattern="^.ezanvakti ?(.*)")
async def ezanvakti(event):
    konum = event.pattern_match.group(1).lower()

    if len(konum) < 1:
        await event.edit("`Lütfen komutun yanına bir şehir belirtin.`")
        return

    url = f'https://quiec.tech/ezan.php?il={konum}'
    request = requests.get(url)
    result = json.loads(request.text)

    if result[0] == '404':
        await event.edit(f"`{konum} için bir bilgi bulunamadı.`")
        return
        
    imsak = result[0]
    gunes = result[1]
    ogle = result[2]
    ikindi = result[3]
    aksam = result[4]
    yatsi = result[5]

    vakitler =(f"**Diyanet Namaz Vakitleri**\n\n" + 
                 f"📍 **Yer: **`{konum}`\n\n" +
                 f"🏙 **İmsak: ** `{imsak}`\n" +
                 f"🌅 **Güneş: ** `{gunes}`\n" +
                 f"🌇 **Öğle: ** `{ogle}`\n" +
                 f"🌆 **İkindi: ** `{ikindi}`\n" +
                 f"🌃 **Akşam: ** `{aksam}`\n" +
                 f"🌌 **Yatsı: ** `{yatsi}`\n")

    await event.edit(vakitler)

CMD_HELP.update({
    "ezanvakti":
    ".ezanvakti <şehir> \
    \nKullanım: Belirtilen şehir için namaz vakitlerini gösterir. \
    \nÖrnek: .ezanvakti istanbul"
})
