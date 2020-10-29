# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


import aiohttp
from userbot.events import register
from userbot import CMD_HELP
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("github")

# ████████████████████████████████ #

@register(pattern=r".git (.*)", outgoing=True)
async def github(event):
    URL = f"https://api.github.com/users/{event.pattern_match.group(1)}"
    chat = await event.get_chat()
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                await event.reply("`" + event.pattern_match.group(1) +
                                  LANG['NOT_FOUND'])
                return

            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            bio = result.get("bio", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = f"`{event.pattern_match.group(1)} {LANG['INFO']}:`\
            \n{LANG['NAME']}: `{name}`\
            \nBio: `{bio}`\
            \nURL: {url}\
            \n{LANG['COMPANY']}: `{company}`\
            \n{LANG['CREATED']}: `{created_at}`"

            if not result.get("repos_url", None):
                await event.edit(REPLY)
                return
            async with session.get(result.get("repos_url", None)) as request:
                result = request.json
                if request.status == 404:
                    await event.edit(REPLY)
                    return

                result = await request.json()

                REPLY += f"\n{LANG['REPOS']}\n"

                for nr in range(len(result)):
                    REPLY += f"[{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"

                await event.edit(REPLY)

CmdHelp('git').add_command(
    'git', '<kullanıcı adı>', 'Hedeflenen kişinin GitHub bilgilerini gösterir.', 'git quiec'
).add()