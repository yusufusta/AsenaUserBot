# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the  GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta



import asyncio
import time
from telethon.tl import functions

from userbot import CMD_HELP, ASYNC_POOL
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("auto")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.auto ?(.*)")
async def auto(event):
    metod = event.pattern_match.group(1).lower()
    
    if str(metod) != "isim" and str(metod) != "bio":
        await event.edit(LANG['INVALID_TYPE'])
        return

    if metod in ASYNC_POOL:
        await event.edit(LANG['ALREADY'] % metod)
        return

    await event.edit(LANG['SETTING'] % metod)
    if metod == "isim":
        HM = time.strftime("%H:%M")

        await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            last_name=LANG['NAME'] % HM
        ))
    elif metod == "bio":
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M")

        Bio = LANG['BIO'].format(tarih=DMY, saat=HM) + LANG['NICK'] 
        await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            about=Bio
        ))


    await event.edit(LANG['SETTED'] % metod)

    ASYNC_POOL.append(metod)

    while metod in ASYNC_POOL:
        try:
            if metod == "isim":
                HM = time.strftime("%H:%M")

                await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    last_name=LANG['NAME'] % HM
                ))
            elif metod == "bio":
                DMY = time.strftime("%d.%m.%Y")
                HM = time.strftime("%H:%M")

                Bio = LANG['BIO'].format(tarih=DMY, saat=HM) + LANG['NICK'] 
                await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    about=Bio
                ))

            await asyncio.sleep(60)
        except:
            return

CmdHelp('auto').add_command(
    'auto', 'isim ya da bio', 'Otomatik saate göre değiştirir', '.auto isim'
).add()