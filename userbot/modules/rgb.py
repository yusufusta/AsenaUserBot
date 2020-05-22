# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

# @NaytSeyd tarafından portlanmıştır.
#

import io
import os
import random
import textwrap

from PIL import Image, ImageChops, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument
from userbot.events import register 
from userbot import CMD_HELP, bot

@register(outgoing=True, pattern="^.rgb(?: |$)(.*)")
async def sticklet(event):
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)

    # Giriş metnini al
    sticktext = event.pattern_match.group(1).strip()

    if len(sticktext) < 1:
        await event.edit("`Lütfen komutun yanına bir metin yazın`")
        return

    # Komutu düzenle
    await event.edit("`Resme dönüştürülüyor...`")

    # https://docs.python.org/3/library/textwrap.html#textwrap.wrap
    sticktext = textwrap.wrap(sticktext, width=10)
    # Listeyi bir dizeye dönüştür
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = await get_font_file(event.client, "@FontRes")

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 10
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "@resim.webp"

    def trim(im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        return im.crop(bbox) if bbox else im

    image = trim(image)
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    # mesajı sil
    await event.delete()

    await event.client.send_file(event.chat_id, image_stream, reply_to=event.message.reply_to_msg_id)
    # Temizlik
    try:
        os.remove(FONT_FILE)
    except:
        pass


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
    "rgb": 
    ".rgb \
    \nKullanım: Metninizi RGB çıkartmaya dönüştürün.\n"
})
