# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Çıkartma oluşturmak ya da çalmak için yapılmış UserBot modülüdür. Teşekkürler @rupansh """

import io
import math
import urllib.request
from os import remove
from PIL import Image
import random
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto
from userbot import bot, CMD_HELP
from userbot.events import register
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID
from telethon.tl.types import DocumentAttributeSticker

DIZCILIK_STR = [
    "Çıkartmayı dızlıyorum...",
    "Yaşasın dızcılık...",
    "Bu çıkartmayı kendi paketime davet ediyorum...",
    "Bunu dızlamam lazım...",
    "Hey bu güzel bir çıkartma!\nHemen dızlıyorum..",
    "Çıkartmanı dızlıyorum\nhahaha.",
    "Hey şuraya bak. (☉｡☉)!→\nBen bunu dızlarken...",
    "Güller kırmızı menekşeler mavi, bu çıkartmayı paketime dızlayarak havalı olacağım...",
    "Çıkartma hapsediliyor...",
    "Bay dızcı bu çıkartmayı dızlıyor... ",
]


@register(outgoing=True, pattern="^.dızla")
async def dizla(args):
    """ .dızla komutu çıkartmaları başka paketten alır ya da yeni bir çıkartma oluşturur. """
    user = await bot.get_me()
    if not user.username:
        user.username = user.first_name
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None

    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            await args.edit(f"`{random.choice(DIZCILIK_STR)}`")
            photo = io.BytesIO()
            photo = await bot.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split('/'):
            await args.edit(f"`{random.choice(DIZCILIK_STR)}`")
            photo = io.BytesIO()
            await bot.download_file(message.media.document, photo)
            if (DocumentAttributeFilename(file_name='sticker.webp') in
                    message.media.document.attributes):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            await args.edit(f"`{random.choice(DIZCILIK_STR)}`")
            await bot.download_file(message.media.document,
                                    'AnimatedSticker.tgs')

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt

            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await args.edit("`Desteklenmeyen dosya!`")
            return
    else:
        await args.edit("`Bunu dızlayamam...`")
        return

    if photo:
        splat = args.text.split()
        if not emojibypass:
            emoji = "🤔"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]  # Kullanıcı ikisini de gönderebilir
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                # Kullanıcı başka pakete eklemek istiyor.
                pack = int(splat[1])
            else:
                # Kullanıcı sadece özel emoji istedi, varsayılan pakete eklemek istiyor.
                emoji = splat[1]

        packname = f"a{user.id}_by_{user.username}_{pack}"
        packnick = f"@{user.username}'s UserBot pack {pack}"
        cmd = '/newpack'
        file = io.BytesIO()

        if not is_anim:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        else:
            packname += "_anim"
            packnick += " (Animasyonlu)"
            cmd = '/newanimated'

        response = urllib.request.urlopen(
            urllib.request.Request(f'http://t.me/addstickers/{packname}'))
        htmlstr = response.read().decode("utf8").split('\n')

        if "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>." not in htmlstr:
            async with bot.conversation('Stickers') as conv:
                await conv.send_message('/addsticker')
                await conv.get_response()
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while "120" in x.text:
                    pack += 1
                    packname = f"a{user.id}_by_{user.username}_{pack}"
                    packnick = f"@{user.username}'s UserBot pack {pack}"
                    await args.edit("`Yetersiz paket alanından dolayı " + str(pack) +
                                    " numaralı pakete geçiliyor`")
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Geçersiz paket seçildi.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file('AnimatedSticker.tgs')
                            remove('AnimatedSticker.tgs')
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await conv.get_response()
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Kullanıcının sürekli bildirim almamasını sağlar.
                        await bot.send_read_acknowledge(conv.chat_id)
                        await args.edit(f"`Çıkartma başka bir pakete eklendi.\
                            \nBu paket yeni oluşturuldu.\
                            \nYeni paket [burada](t.me/addstickers/{packname}) bulunabilir.",
                                        parse_mode='md')
                        return
                if is_anim:
                    await conv.send_file('AnimatedSticker.tgs')
                    remove('AnimatedSticker.tgs')
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await args.edit(
                        "`Çıkartma ekleme başarısız, ` @Stickers `botu ile elle eklemeyi deneyin.`"
                    )
                    return
                await conv.send_message(emoji)
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message('/done')
                await conv.get_response()
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
        else:
            await args.edit("`Yeni paket oluşturuluyor...`")
            async with bot.conversation('Stickers') as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file('AnimatedSticker.tgs')
                    remove('AnimatedSticker.tgs')
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await args.edit(
                        "`Çıkartma ekleme başarısız, ` @Stickers `botu ile elle eklemeyi deneyin.`"
                    )
                    return
                await conv.send_message(emoji)
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Kullanıcının sürekli bildirim almamasını sağlar.
                await bot.send_read_acknowledge(conv.chat_id)

        await args.edit(f"`Çıkartma başarıyla pakete eklendi.`\
            \nPaket [şurada](t.me/addstickers/{packname}) bulunabilir.",
                        parse_mode='md')


async def resize_photo(photo):
    """ Fotoğrafı 512x512 boyutuna getirir. """
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


@register(outgoing=True, pattern="^.dızbilgisi$")
async def dizbilgisi(event):
    if not event.is_reply:
        await event.edit("`Hiçlikten bir bilgi çekemem, sence yapabilir miyim?!`")
        return

    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await event.edit("`Paket detaylarını görmek için bir çıkartmayı yanıtlayın`")
        return

    try:
        stickerset_attr = rep_msg.document.attributes[1]
        await event.edit(
            "`Bu paketten detaylar alınıyor, lütfen bekleyin..`")
    except BaseException:
        await event.edit("`Bu bir çıkartma değil. Bir çıkartmayı yanıtlayın.`")
        return

    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        await event.edit("`Bu bir çıkartma değil. Bir çıkartmayı yanıtlayın.`")
        return

    get_stickerset = await bot(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash)))
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)

    OUTPUT = f"**Sticker başlığı:** `{get_stickerset.set.title}\n`" \
        f"**Sticker kısa adı:** `{get_stickerset.set.short_name}`\n" \
        f"**Resmi mi:** `{get_stickerset.set.official}`\n" \
        f"**Arşivlenmiş mi:** `{get_stickerset.set.archived}`\n" \
        f"**Paketteki çıkartma sayısı:** `{len(get_stickerset.packs)}`\n" \
        f"**Paketteki emoji sayısı:**\n{' '.join(pack_emojis)}"

    await event.edit(OUTPUT)


CMD_HELP.update({
    "stickers":
    ".dızla\
\nKullanım: .dızla ile bir çıkartmaya ya da resme yanıtlayarak kendi çıkartma paketinize çıkartma olarak ekleyebilirsiniz.\
\n\n.dızla [emoji(ler)]\
\nKullanım: .dızla gibi çalışır fakat istediğiniz emojiyi çıkartmanın emojisi olarak belirtir.\
\n\n.dızla [numara]\
\nKullanım: Çıkartmayı ya da resmi belirtilen pakete ekler fakat emoji olarak şu kullanılır: 🤔 \
\n\n.dızla [emoji(ler)] [numara]\
\nKullanım: Çıkartmayı ya da resmi belirtilen pakete ekler ve belirttiğiniz emoji çıkartmanın emojisi olarak kullanılır.\
\n\n.dızbilgisi\
\nKullanım: Çıkartma paketi hakkında bilgi verir."
})
