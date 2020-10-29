# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

from userbot import CMD_HELP
from userbot.events import register
from PIL import Image
import io
import os
import asyncio
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("liste")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.liste ?(gmute|gban)?")
async def liste(event):
    liste = event.pattern_match.group(1)
    try:
        if len(liste) < 1:
            await event.edit(LANG['WRONG_INPUT'])
            return
    except:
        await event.edit(LANG['WRONG_INPUT'])
        return
    
    if liste == "gban":
        try:
            from userbot.modules.sql_helper.gban_sql import gbanlist
        except:
            await event.edit(LANG['NEED_SQL_MODE'])
            return
        await event.edit(LANG['GBANNED_USERS'])
        mesaj = ""
        for user in gbanlist():
            mesaj += f"**ID: **`{user.sender}`\n"

        if len(mesaj) > 4000:
            await event.edit(LANG['TOO_MANY_GBANNED'])
            open("gban_liste.txt", "w+").write(mesaj)
            await event.client.send_message(event.chat_id, LANG['GBAN_TXT'], file="gban_liste.txt")
            os.remove("gban_liste.txt")
        else:
            await event.edit(LANG['GBAN_LIST'] % mesaj)
    elif liste == "gmute":
        try:
            from userbot.modules.sql_helper.gmute_sql import gmutelist
        except:
            await event.edit(LANG['NEED_SQL_MODE'])
            return
        await event.edit(LANG['GMUTE_DATA'])
        mesaj = ""
        for user in gmutelist():
            mesaj += f"**ID: **`{user.sender}`\n"

        if len(mesaj) > 4000:
            await event.edit(LANG['TOO_MANY_GMUTED'])
            open("gmute_liste.txt", "w+").write(mesaj)
            await event.client.send_message(event.chat_id, LANG['GMUTE_TXT'], file="gmute_liste.txt")
            os.remove("gmute_liste.txt")
        else:
            await event.edit(LANG['GMUTE_LIST'] % mesaj)

CmdHelp('liste').add_command(
    'liste', '<gmute/gban>', 'Gbanladığınız ya da Gmutelediğiniz kişileri getirir.'
).add()