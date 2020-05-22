# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta
#
# @NaytSeyd tarafından portlanmıştır.
# @frknkrc44 tarafından düzenlenmiştir.
#

import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.tl import functions
from telethon.tl.types import InputMessagesFilterDocument
from userbot import CMD_HELP, AUTO_PP, ASYNC_POOL
from userbot.events import register
import asyncio
import random
import shutil

@register(outgoing=True, pattern="^.autopp ?(.*)")
async def autopic(event):
    if 'autopic' in ASYNC_POOL:
        await event.edit("`Görünüşe göre profil fotoğrafınız zaten otomatik olarak değişiyor.`")
        return

    await event.edit("`Profil fotoğrafınız ayarlanıyor ...`")

    FONT_FILE_TO_USE = await get_font_file(event.client, "@FontDunyasi")

    downloaded_file_name = "./userbot/eskipp.png"
    downloader = SmartDL(AUTO_PP, downloaded_file_name, progress_bar=True)
    downloader.start(blocking=False)
    photo = "yenipp.png"
    while not downloader.isFinished():
        continue

    await event.edit("`Profil fotoğrafınız ayarlandı :)`")

    ASYNC_POOL.append('autopic')

    while 'autopic' in ASYNC_POOL:
        shutil.copy(downloaded_file_name, photo)
        current_time = datetime.now().strftime("%H:%M")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 70)
        size = drawn_text.multiline_textsize(current_time, font=fnt)
        drawn_text.text(((img.width - size[0]) / 2, (img.height - size[1])),
                       current_time, font=fnt, fill=(255, 255, 255))
        img.save(photo)
        file = await event.client.upload_file(photo)  # pylint:disable=E0602
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
                file
            ))
            os.remove(photo)
            await asyncio.sleep(60)
        except:
            return

async def get_font_file(client, channel_id):
    # Önce yazı tipi mesajlarını al
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        # Bu işlem çok fazla kullanıldığında
        # "FLOOD_WAIT" yapmaya neden olabilir
        limit=None
    )
    # Yazı tipi listesinden rastgele yazı tipi al
    # https://docs.python.org/3/library/random.html#random.choice
    font_file_message = random.choice(font_file_message_s)
    # Dosya yolunu indir ve geri dön
    return await client.download_media(font_file_message)

CMD_HELP.update({
    "autopp": 
    ".autopp \
    \nKullanım: Bu komut belirlediğiniz fotoğrafı profil resmi yapar \
    \nve bir saat ekler. Bu saat her dakika değişir. \
    \nNOT: Küçük bir ihtimal bile olsa ban yeme riskiniz var. Bu yüzden dikkatli kullanın."
})
