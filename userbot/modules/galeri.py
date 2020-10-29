# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

import re
import asyncio

from userbot import CMD_HELP, ASYNC_POOL, GALERI_SURE
from userbot.events import register
from userbot.main import FotoDegistir
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("galeri")

# ████████████████████████████████ #

URL_REGEX = re.compile(
    # https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@register(outgoing=True, pattern="^.galeri ?(.*)")
async def galeri(event):
    try:
        import userbot.modules.sql_helper.galeri_sql as sql
    except:
        await event.edit("`SQL dışı mod'ta galeri çalışmaz!`")
    secenek = event.pattern_match.group(1)
    secen = secenek.split(" ")
    if secen[0] == "ekle":
        if len(secen) > 1:
            URL = re.search(URL_REGEX, secen[1])
            if URL != None:
                sql.ekle_foto(secen[1])
                sql.getir_foto()
                await event.edit(LANG['ADDED_LIST'])
            else:
                await event.edit(LANG['INVALID_URL'])
        else:
            await event.edit(LANG['EXAMPLE'])
    elif secen[0] == "liste":
        yfoto = ""
        sql.getir_foto()
        fotolar = sql.TUM_GALERI
        for foto in fotolar:
            yfoto += f"\n▶️ ({foto.g_id}) [Fotoğraf]({foto.foto})"
        await event.edit(f"**{LANG['LIST']}**\n" + yfoto)
    elif secen[0] == "sil":
        if secen[1].isdigit():
            silme = sql.sil_foto(secen[1])
            if silme == True:
                await event.edit(LANG['REMOVED'])
            else:
                await event.edit(f"{LANG['REMOVED_ERROR']}: {silme}")
        else:
            await event.edit(f"**{LANG['NEED_NUMBER']}** `.galeri sil 2`")
    elif secen[0] == "başla":
        if "galeri" in ASYNC_POOL:
            await event.edit(LANG['WORKING'])
            return
        ASYNC_POOL.append("galeri")
        sql.getir_foto()
        await event.edit(LANG['STARTED'])
        if len(sql.TUM_GALERI) >= 1:
            while "galeri" in ASYNC_POOL:
                fotolar = sql.TUM_GALERI
                i = 0
                while i < len(fotolar):
                    if not "galeri" in ASYNC_POOL:
                        break
                    if i == len(fotolar):
                        i = 0
                    await FotoDegistir(i)
                    await asyncio.sleep(GALERI_SURE)
                    i += 1
        else:
            await event.edit(LANG['NEED_PHOTO'])
            return
    elif secen[0] == "kapa":
        if "galeri" in ASYNC_POOL:
            ASYNC_POOL.remove("galeri")
            await event.edit(LANG['STOPPED'])
        else:
            event.edit(LANG['ALREADY_STOP'])
        return
    else:
        await event.edit(LANG['INVALID'])

CmdHelp('galeri').add_command(
    'galeri ekle', '<url>', 'Galeri sırasına fotoğraf ekler', 'galeri ekle https://i.hizliresim.com/wFSVKd.jpg'
).add_command(
    'galeri liste', None, 'Galeri sırasını gösterir.'
).add_command(
    'galeri sil', '<sayı>', 'Galeri sırasından bir resmi siler.', 'galeri sil 4'
).add()