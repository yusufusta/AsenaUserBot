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

# @NaytSeyd tarafından portlanmıştır.

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.q(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Herhangi bir kullanıcı mesajına cevap verin.`")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("`Mesaja cevap verin.`")
       return
    chat = "@QuotLyBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("`Botlara cevap veremezsiniz.`")
       return
    await event.edit("`Alıntı yapılıyor...`")

    async with bot.conversation(chat, exclusive=False, replies_are_responses=True) as conv:
          response = None
          try:
              msg = await reply_message.forward_to(chat)
              response = await conv.get_response(message=msg, timeout=5)
          except YouBlockedUserError: 
              await event.edit("`Lütfen @QuotLyBot engelini kaldırın ve tekrar deneyin`")
              return
          except Exception as e:
              print(e.__class__)

          if not response:
              await event.edit("`Botdan cevap alamadım!`")
          elif response.text.startswith("Merhaba!"):
             await event.edit("`Gizlilik ayarları yüzenden alıntı yapamadım`")
          else: 
             await event.delete()
             await response.forward_to(event.chat_id)
          await conv.mark_read()
          await conv.cancel_all()

CMD_HELP.update({
    "quotly": 
    ".q \
    \nKullanım: Metninizi çıkartmaya dönüştürün.\n"
})
