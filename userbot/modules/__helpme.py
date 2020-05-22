# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta
#

# @Qulec tarafından yazılmıştır.
# Thanks @Spechide.

import asyncio
import json
import logging
import requests
import userbot

from userbot import CMD_HELP, BOT_USERNAME
from userbot.events import register

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

@register(outgoing=True, pattern="^.yardım")
async def yardim(event):
    tgbotusername = BOT_USERNAME
    if tgbotusername is not None:
        results = await event.client.inline_query(
            tgbotusername,
            "@AsenaUserBot"
        )
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
        await event.delete()
    else:
        await event.edit("`Bot çalışmıyor! Lütfen Bot Tokeni ve Kullanıcı adını doğru ayarlayın. Modül durduruldu.`")
