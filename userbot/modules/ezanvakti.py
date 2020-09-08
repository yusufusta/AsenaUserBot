# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

# @NaytSeyd tarafından portlanmıştır.
# @frknkrc44 tarafından düzenlenmiştir.

import json
import logging

import requests
from userbot import CMD_HELP
from userbot.events import register

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("ezanvakti")

# ████████████████████████████████ #


@register(outgoing=True, pattern="^.ezanvakti ?(.*)")
async def ezanvakti(event):
    konum = event.pattern_match.group(1).lower()

    if len(konum) < 1:
        await event.edit(LANG['NEED_CITY'])
        return

    url = f'https://api.quiec.tech/namaz.php?il={konum}'
    request = requests.get(url)
    result = json.loads(request.text)

    if result[0] == '404':
        await event.edit(f"`{konum} {LANG['NOT_FOUND']}`")
        return
        
    imsak = result[0]
    gunes = result[1]
    ogle = result[2]
    ikindi = result[3]
    aksam = result[4]
    yatsi = result[5]

    vakitler =(f"**{LANG['DIYANET']}**\n\n" + 
                 f"📍 **{LANG['LOCATION']}: **`{konum}`\n\n" +
                 f"🏙 **{LANG['IMSAK']}: ** `{imsak}`\n" +
                 f"🌅 **{LANG['GUNES']}: ** `{gunes}`\n" +
                 f"🌇 **{LANG['OGLE']}: ** `{ogle}`\n" +
                 f"🌆 **{LANG['IKINDI']}: ** `{ikindi}`\n" +
                 f"🌃 **{LANG['AKSAM']}: ** `{aksam}`\n" +
                 f"🌌 **{LANG['YATSI']}: ** `{yatsi}`\n")

    await event.edit(vakitler)

CMD_HELP.update({
    "ezanvakti":
    ".ezanvakti <şehir> \
    \nKullanım: Belirtilen şehir için namaz vakitlerini gösterir. \
    \nÖrnek: .ezanvakti istanbul"
})
