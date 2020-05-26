# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta
# @Qulec tarafından yazılmıştır.
#

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.events import register
from userbot import bot, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from time import sleep
import os
from telethon.tl.types import MessageMediaPhoto
import asyncio


def is_message_image(message):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            return True
        if message.media.document:
            if message.media.document.mime_type.split("/")[0] == "image":
                return True
        return False
    return False
    
async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


@register(outgoing=True, pattern="^.sangmata(?: |$)(.*)")
async def sangmata(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Herhangi bir kullanıcı mesajına cevap verin.`")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("`Mesaja cevap verin.`")
       return
    chat = "@SangMataInfo_bot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("`Botlara cevap veremezsiniz.`")
       return
    await event.edit("`İşleniyor...`")
    async with bot.conversation(chat, exclusive=False) as conv:
          response = None
          try:
              msg = await reply_message.forward_to(chat)
              response = await conv.get_response(message=msg, timeout=5)
          except YouBlockedUserError: 
              await event.edit(f"`Lütfen {chat} engelini kaldırın ve tekrar deneyin`")
              return
          except Exception as e:
              print(e.__class__)

          if not response:
              await event.edit("`Botdan cevap alamadım!`")
          elif response.text.startswith("Forward"):
             await event.edit("`Gizlilik ayarları yüzenden alıntı yapamadım`")
          else: 
             await event.edit(response.text)
          sleep(1)
          await bot.send_read_acknowledge(chat, max_id=(response.id+3))
          await conv.cancel_all()

thumb_image_path = TEMP_DOWNLOAD_DIRECTORY + "/THUMB.png"
@register(outgoing=True, pattern="^.meme (.*)")
async def memeyap(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Kullanım: Lütfen bir mesaja yanıt vererek yazın. Örnek: .meme üst;alt`")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("```Bir Fotoğraf/sticker/gif'e yanıt verin.```")
       return
    chat = "@MemeAutobot"
    sender = reply_message.sender
    file_ext_ns_ion = "@memetime.png"
    file = await event.client.download_file(reply_message.media)
    uploaded_gif = None
    if reply_message.sender.bot:
       await event.edit("```Gerçek bir kullanıcının mesajına yanıt verin.```")
       return
    else:
     await event.edit("```Memeleniyor! (」ﾟﾛﾟ)｣ ```")
    
    async with event.client.conversation(chat) as bot_conv:
          try:
            memeVar = str(event.pattern_match.group(1))
            memeVar = memeVar.strip()
            await silently_send_message(bot_conv, "/start")
            await asyncio.sleep(1)
            await silently_send_message(bot_conv, memeVar)
            await event.client.send_file(chat, reply_message.media)
            response = await bot_conv.get_response()
          except YouBlockedUserError: 
              await event.reply("```Lütfen @MemeAutobot engelini kaldırıp tekrar deneyin.```")
              return
          if response.text.startswith("Forward"):
              await event.edit(f"```{response.text}```")
          if "Okay..." in response.text:
            await event.edit("```Bu bir fotoğraf değil! Bekle biraz fotoğrafa çevireceğim.```")
            thumb = None
            if os.path.exists(thumb_image_path):
                thumb = thumb_image_path
            input_str = event.pattern_match.group(1)
            if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
                os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
            if event.reply_to_msg_id:
                file_name = "meme.png"
                reply_message = await event.get_reply_message()
                to_download_directory = TEMP_DOWNLOAD_DIRECTORY
                downloaded_file_name = os.path.join(to_download_directory, file_name)
                downloaded_file_name = await event.client.download_media(
                    reply_message,
                    downloaded_file_name,
                    )
                if os.path.exists(downloaded_file_name):
                    await event.client.send_file(
                        chat,
                        downloaded_file_name,
                        force_document=False,
                        supports_streaming=False,
                        allow_cache=False,
                        thumb=thumb,
                        )
                    os.remove(downloaded_file_name)
                else:
                    await event.edit("Dosya bulunamadı {}.".format(input_str))
            response = await bot_conv.get_response()
            the_download_directory = TEMP_DOWNLOAD_DIRECTORY
            files_name = "memes.webp"
            download_file_name = os.path.join(the_download_directory, files_name)
            await event.client.download_media(
                response.media,
                download_file_name,
                )
            requires_file_name = TEMP_DOWNLOAD_DIRECTORY + "memes.webp"
            await event.client.send_file(  # pylint:disable=E0602
                event.chat_id,
                requires_file_name,
                supports_streaming=False,
                caption="Memified using @MemeAutoBot",
                # Courtesy: @A_Dark_Princ3
            )
            await event.delete()
          elif not is_message_image(reply_message):
            await event.edit("Bilinmeyen mesaj tipi!")
            return
          else: 
               await event.client.send_file(event.chat_id, response.media)

@register(pattern="^.scan")
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Lütfen bir mesaja yanıt verin.`")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("`Lütfen bir dosyaya yanıt verin.`")
       return
    chat = "@DrWebBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("`Lütfen gerçekten bir kullanıcının mesajına yanıt verin.`")
       return
    await event.edit("`Musallet.exe var mı yok mu bakıyorum...`")
    async with event.client.conversation(chat) as conv:
      try:     
         response = conv.wait_event(events.NewMessage(incoming=True,from_users=161163358))
         await event.client.forward_messages(chat, reply_message)
         response = await response 
      except YouBlockedUserError:
         await event.reply(f"`Mmmh sanırım` {chat} `engellemişsin. Lütfen engeli aç.`")
         return

      if response.text.startswith("Forward"):
         await event.edit("`Gizlilik ayarları yüzenden alıntı yapamadım.`")
      elif response.text.startswith("Select"):
         await event.client.send_message(chat, "English")
         await event.edit("`Lütfen bekleyiniz...`")

         response = conv.wait_event(events.NewMessage(incoming=True,from_users=161163358))
         await event.client.forward_messages(chat, reply_message)
         response = conv.wait_event(events.NewMessage(incoming=True,from_users=161163358))
         response = await response
         
         await event.edit(f"**Virüs taraması bitti. İşte sonuçlar:**\n {response.message.message}")


      elif response.text.startswith("Still"):
         await event.edit(f"`Dosya taranıyor...`")

         response = conv.wait_event(events.NewMessage(incoming=True,from_users=161163358))
         response = await response 
         if response.text.startswith("No threats"):
            await event.edit(f"**Virüs taraması bitti. Bu dosya temiz. Geç!**")
         else:
            await event.edit(f"**Virüs taraması bitti. Whopsie! Bu dosya tehlikeli. Sakın yükleme!**\n\nDetaylı bilgi: {response.message.message}")

@register(pattern="^.voicy")
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Lütfen bir mesaja yanıt verin.`")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("`Lütfen bir dosyaya yanıt verin.`")
       return
    chat = "@Voicybot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("`Lütfen gerçekten bir kullanıcının mesajına yanıt verin.`")
       return
    await event.edit("`Ses dinleniyor... Erkan enegtarlar...`")
    async with event.client.conversation(chat) as conv:
        try:     
            await event.client.forward_messages(chat, reply_message)
        except YouBlockedUserError:
            await event.reply(f"`Mmmh sanırım` {chat} `engellemişsin. Lütfen engeli aç.`")
            return
      
        response = conv.wait_event(events.MessageEdited(incoming=True,from_users=259276793))
        response = await response
        if response.text.startswith("__👋"):
            await event.edit("`Botu başlatıp Türkçe yapmanız gerekmektedir.`")
        elif response.text.startswith("__👮"):
            await event.edit("`Ses bozuk, ses. Ne dediğini anlamadım.`")
        else:
            await event.edit(f"**Bir şeyler duydum: **`{response.text}`")

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
    "sangmata": 
    ".sangmata \
    \nKullanım: Belirtilen kullanıcının isim geçmişini görüntüleyin.\n",
    "drweb": 
    ".drweb \
    \nKullanım: Belirtilen dosyada virüs var mı yok mu bakın.\n",
    "meme": 
    ".meme üst;alt \
    \nKullanım: Fotoğrafa yazı ekleyin.\n",

    "quotly": 
    ".q \
    \nKullanım: Metninizi çıkartmaya dönüştürün.\n"
})
