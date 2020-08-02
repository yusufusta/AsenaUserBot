# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Paperplane module for kanging stickers or making new ones. """

import io
import math
import urllib.request
from PIL import Image

from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto, InputPeerNotifySettings
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot, PAKET_ISMI
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from telethon import events

PACK_FULL = "Whoa! That's probably enough stickers for one pack, give it a break. \
A pack can't have more than 120 stickers at the moment."
PACK_DOESNT_EXIST = "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."


@register(outgoing=True, pattern="^.dızla($| )?((?![0-9]).+?)? ?([0-9]*)?")
async def kang(event):
    await event.edit(f"`{PLUGIN_MESAJLAR['dızcı']}`")
    user = await bot.get_me()
    pack_username = ''
    if not user.username:
        try:
            user.first_name.decode('ascii')
            pack_username = user.first_name
        except UnicodeDecodeError: # User's first name isn't ASCII, use ID instead
            pack_username = user.id
    else: pack_username = user.username

    textx = await event.get_reply_message()
    emoji = event.pattern_match.group(2)
    number = int(event.pattern_match.group(3) or 1) # If no number specified, use 1
    new_pack = False

    if textx.photo or textx.sticker: message = textx
    elif event.photo or event.sticker: message = event
    else:
        await event.edit("`Dızlayabilmem için bana sticker veya fotoğraf vermen gerek!`")
        return

    sticker = io.BytesIO()
    await bot.download_media(message, sticker)
    sticker.seek(0)

    if not sticker:
        await event.edit("`Sticker indirilemedi! Fotoğraf veya sticker gönderdiğinize emin olun.`")
        return

    is_anim = message.file.mime_type == "application/x-tgsticker"
    if not is_anim:
        img = await resize_photo(sticker)
        sticker.name = "sticker.png"
        sticker.seek(0)
        img.save(sticker, "PNG")

    # The user didn't specify an emoji...
    if not emoji:
        if message.file.emoji: # ...but the sticker has one
            emoji = message.file.emoji
        else: # ...and the sticker doesn't have one either
            emoji = "🤔"

    packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
    packtitle = (f"@{user.username or user.first_name} {PAKET_ISMI} "
                f"{number}{' animasyonlu' if is_anim else ''}")
    response = urllib.request.urlopen(
            urllib.request.Request(f'http://t.me/addstickers/{packname}'))
    htmlstr = response.read().decode("utf8").split('\n')
    new_pack = PACK_DOESNT_EXIST in htmlstr

    if new_pack:
        await event.edit("`Sticker paketi oluşturulmamış! Yeni paket oluşturuluyor...`")
        await newpack(is_anim, sticker, emoji, packtitle, packname, message)
    else:
        async with bot.conversation("Stickers") as conv:
            # Cancel any pending command
            await conv.send_message('/cancel')
            await conv.get_response()

            # Send the add sticker command
            await conv.send_message('/addsticker')
            await conv.get_response()

            # Send the pack name
            await conv.send_message(packname)
            x = await conv.get_response()

            # Check if the selected pack is full
            while x.text == PACK_FULL:
                # Switch to a new pack, create one if it doesn't exist
                number += 1
                packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
                packtitle = (f"@{user.username or user.first_name} {PAKET_ISMI} "
                            f"{number}{' animated' if is_anim else ''}")

                await event.edit(
                    f"`Yetersiz paket alanından dolayı {number} sayılı pakete geçiliyor...`"
                )

                await conv.send_message(packname)
                x = await conv.get_response()
                if x.text == "Invalid pack selected.": # That pack doesn't exist
                    await newpack(is_anim, sticker, emoji, packtitle, packname)

                    # Read all unread messages
                    await bot.send_read_acknowledge("stickers")
                    # Unmute Stickers bot back
                    muted = await bot(UpdateNotifySettingsRequest(
                        peer=429000,
                        settings=InputPeerNotifySettings(mute_until=None))
                    )

                    await event.edit(
                        f"`Sticker {number}{'(animasyonlu)' if is_anim else ''} sayılı pakete eklendi, "
                        f"{emoji} emojisi ile birlikte! "
                        f"Paket `[burada](t.me/addstickers/{packname})`bulunabilinir.`",
                        parse_mode='md')
                    return

            # Upload the sticker file
            if is_anim:
                upload = await message.client.upload_file(sticker, file_name="AnimatedSticker.tgs")
                await conv.send_file(upload, force_document=True)
            else:
                sticker.seek(0)
                await conv.send_file(sticker, force_document=True)
            kontrol = await conv.get_response()
        
            if "Sorry, the image dimensions are invalid." in kontrol.text:
                await event.edit("`Sticker's kabul etmedi. İkinci yöntem deneniyor...`")
                try:
                    await bot.send_file("@ezstickerbot", message, force_document=True)
                except YouBlockedUserError:
                    return await event.edit("`Lütfen` @EzStickerBot `engelini açın ve tekrar deneyin!`")

                response = await conv.wait_event(events.NewMessage(incoming=True,from_users=350549033))
                await bot.send_read_acknowledge(350549033)
                await event.client.forward_messages("stickers", response.message, 350549033)

            # Send the emoji
            await conv.send_message(emoji)
            await conv.get_response()

            # Finish editing the pack
            await conv.send_message('/done')
            await conv.get_response()

    # Read all unread messages
    await bot.send_read_acknowledge(429000)
    # Unmute Stickers bot back
    muted = await bot(UpdateNotifySettingsRequest(
        peer=429000,
        settings=InputPeerNotifySettings(mute_until=None))
    )

    await event.edit(
        f"`Sticker {number}{'(animasyonlu)' if is_anim else ''} sayılı pakete eklendi, "
        f"{emoji} emojisi ile birlikte! "
        f"Paket `[burada](t.me/addstickers/{packname})` bulunabilinir.`",
        parse_mode='md')


async def newpack(is_anim, sticker, emoji, packtitle, packname, message):
    async with bot.conversation("stickers") as conv:
        # Cancel any pending command
        await conv.send_message('/cancel')
        await conv.get_response()

        # Send new pack command
        if is_anim:
            await conv.send_message('/newanimated')
        else:
            await conv.send_message('/newpack')
        await conv.get_response()

        # Give the pack a name
        await conv.send_message(packtitle)
        await conv.get_response()

        # Upload sticker file
        if is_anim:
            upload = await bot.upload_file(sticker, file_name="AnimatedSticker.tgs")
            await conv.send_file(upload, force_document=True)
        else:
            sticker.seek(0)
            await conv.send_file(sticker, force_document=True)
        kontrol = await conv.get_response()
        
        if "Sorry, the image dimensions are invalid." in kontrol.text:
            await bot.send_file("@ezstickerbot", message, force_document=True)
            response = await conv.wait_event(events.NewMessage(incoming=True,from_users=350549033))
            await bot.send_read_acknowledge(350549033)
            await bot.forward_messages(429000, response.message, 350549033)

        # Send the emoji
        await conv.send_message(emoji)
        await conv.get_response()

        # Publish the pack
        await conv.send_message("/publish")
        if is_anim:
            await conv.get_response()
            await conv.send_message(f"<{packtitle}>")
        await conv.get_response()

        # Skip pack icon selection
        await conv.send_message("/skip")
        await conv.get_response()

        # Send packname
        await conv.send_message(packname)
        await conv.get_response()

async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


CMD_HELP.update({
    "stickers":
    ".dızla\
\nKullanım: .dızla ile bir çıkartmaya ya da resme yanıtlayarak kendi çıkartma paketinize çıkartma olarak ekleyebilirsiniz.\
\n\n.dızla [emoji(ler)]\
\nKullanım: .dızla gibi çalışır fakat istediğiniz emojiyi çıkartmanın emojisi olarak belirtir.\
\n\n.dızla [numara]\
\nKullanım: Çıkartmayı ya da resmi belirtilen pakete ekler fakat emoji olarak şu kullanılır: 🤔 \
\n\n.dızla [emoji(ler)] [numara]\
\nKullanım: Çıkartmayı ya da resmi belirtilen pakete ekler ve belirttiğiniz emoji çıkartmanın emojisi olarak kullanılır."})