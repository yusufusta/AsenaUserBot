# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

# @NaytSeyd tarafından portlanmıştır.
# @frknkrc44 tarafından düzenlenmiştir.

import requests
from userbot import CMD_HELP
from userbot.events import register
from bs4 import BeautifulSoup
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("ezanvakti")

# ████████████████████████████████ #


@register(outgoing=True, pattern="^.ezanvakti ?(\w*)")
async def ezanvakti(event):
    konum = event.pattern_match.group(1).lower()
    if not event.text.partition(konum)[2] == '':
        ilce = event.text.partition(konum)[2]
    else:
        ilce = None

    if len(konum) < 1:
        await event.edit(LANG['NEED_CITY'])
        return

    url = f'https://www.mynet.com/{konum}/namaz-vakitleri'
    if not ilce == None:
        url += '/' + ilce.strip()

    request = requests.get(url)
    if not request.status_code == 200:
        await event.edit(f"`{konum} {LANG['NOT_FOUND']}`")
        return

    bs4 = BeautifulSoup(
        request.text, 'lxml'
    )

    result = bs4.find('div', {'class': 'prayer-timeline'}).find_all('div')
    imsak = result[0].find('span', {'class': 'time'}).get_text().strip()
    gunes = result[1].find('span', {'class': 'time'}).get_text().strip()
    ogle = result[2].find('span', {'class': 'time'}).get_text().strip()
    ikindi = result[3].find('span', {'class': 'time'}).get_text().strip()
    aksam = result[4].find('span', {'class': 'time'}).get_text().strip()
    yatsi = result[5].find('span', {'class': 'time'}).get_text().strip()

    vakitler =(f"**{LANG['DIYANET']}**\n\n" + 
                 f"📍 **{LANG['LOCATION']}: **`{konum.capitalize()}/{ilce.strip().capitalize() if not ilce == None else konum.capitalize()}`\n\n" +
                 f"🏙 **{LANG['IMSAK']}: ** `{imsak}`\n" +
                 f"🌅 **{LANG['GUNES']}: ** `{gunes}`\n" +
                 f"🌇 **{LANG['OGLE']}: ** `{ogle}`\n" +
                 f"🌆 **{LANG['IKINDI']}: ** `{ikindi}`\n" +
                 f"🌃 **{LANG['AKSAM']}: ** `{aksam}`\n" +
                 f"🌌 **{LANG['YATSI']}: ** `{yatsi}`\n")

    await event.edit(vakitler)

CmdHelp('ezanvakti').add_command(
    'ezanvakti', '<şehir> <ilçe>', 'Belirtilen şehir için namaz vakitlerini gösterir.', 'ezanvakti ankara etimesgut'
).add()