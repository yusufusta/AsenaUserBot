# Copyright (C) 2020 Yusuf Usta.
# Copyright (C) 2020 RaphielGang.
# Copyright (C) 2020 AsenaUserBot.
#

""" UserBot yardım komutu """

from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.asena(?: |$)(.*)")
async def asena(event):
    """ .asena komutu için """
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Lütfen bir Asena modülü adı belirtin.")
    else:
        await event.edit("Lütfen hangi Asena modülü için yardım istediğinizi belirtin !!\
            \nKullanım: .asena <modül adı>")
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`\n"
        await event.reply(string)
