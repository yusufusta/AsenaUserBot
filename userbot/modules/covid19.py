# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("covid19")

# ████████████████████████████████ #

from userbot import CMD_HELP
from userbot.events import register
from urllib3 import PoolManager
from json import loads as jsloads

@register(outgoing=True, pattern="^.covid$")
async def covid(event):
    try:
        url = 'https://api.quiec.tech/corona.php'
        http = PoolManager()
        request = http.request('GET', url)
        result = jsloads(request.data.decode('utf-8'))
        http.clear()
    except:
        await event.edit(LANG['SOME_ERRORS'])
        return

    sonuclar = (f"** {LANG['SOME_ERRORS']} **\n" +
                f"\n**{LANG['EARTH']}**\n" +
                f"**{LANG['CASE']}** `{result['tum']}`\n" +
                f"**{LANG['DEATH']}** `{result['tumolum']}`\n" +
                f"**{LANG['HEAL']}** `{result['tumk']}`\n" +
                f"\n**{LANG['TR']}**\n" +
                f"**{LANG['TR_ALL_CASES']}** `{result['trtum']}`\n" +
                f"**{LANG['TR_CASES']}** `{result['trbtum']}`\n" +
                f"**{LANG['TR_CASE']}** `{result['tra']}`\n" +
                f"**{LANG['TR_ALL_DEATHS']}** `{result['trolum']}`\n" +
                f"**{LANG['TR_DEATHS']}** `{result['trbolum']}`\n" +
                f"**{LANG['TR_HEAL']}** `{result['trk']}`")

    await event.edit(sonuclar)


CMD_HELP.update({
    "covid19":
    ".covid \
    \nKullanım: Hem Dünya geneli hem de Türkiye için güncel Covid 19 istatistikleri."
})
