# Copyright (C) 2020 TeamDerUntergang.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
