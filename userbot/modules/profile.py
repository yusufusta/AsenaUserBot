# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Telegram'daki profil detaylarınızı değişmeye yarayan UserBot modülüdür. """

import os
from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import (PhotoExtInvalidError,
                                          UsernameOccupiedError)
from telethon.tl.functions.account import (UpdateProfileRequest,
                                           UpdateUsernameRequest)
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          GetUserPhotosRequest,
                                          UploadProfilePhotoRequest)
from telethon.tl.types import InputPhoto, MessageMediaPhoto, User, Chat, Channel
from userbot import bot, CMD_HELP
from userbot.events import register

# ====================== CONSTANT ===============================
INVALID_MEDIA = "```Medya geçerli değil.```"
PP_CHANGED = "```Profil resmi başarıyla değiştirildi.```"
PP_TOO_SMOL = "```Bu resim çok küçük, daha büyük bir resim kullanın.```"
PP_ERROR = "```Resim işlenirken bir hata oluştu.```"

BIO_SUCCESS = "```Biyografi başarıyla değiştirildi.```"

NAME_OK = "```Adın başarıyla değiştirildi.```"
USERNAME_SUCCESS = "```Kullanıcı adın başarıyla değiştirildi.```"
USERNAME_TAKEN = "```Kullanıcı adı müsait değil.```"
# ===============================================================


@register(outgoing=True, pattern="^.reserved$")
async def mine(event):
    """ .reserved komutu ayırdığınız kullanıcı adlarını listeler. """
    result = await bot(GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"{channel_obj.title}\n@{channel_obj.username}\n\n"
    await event.edit(output_str)


@register(outgoing=True, pattern="^.name")
async def update_name(name):
    """ .name komutu Telegram'daki isminizi değişir. """
    newname = name.text[6:]
    if " " not in newname:
        firstname = newname
        lastname = ""
    else:
        namesplit = newname.split(" ", 1)
        firstname = namesplit[0]
        lastname = namesplit[1]

    await name.client(
        UpdateProfileRequest(first_name=firstname, last_name=lastname))
    await name.edit(NAME_OK)


@register(outgoing=True, pattern="^.setpfp$")
async def set_profilepic(propic):
    """ .profilepic komutu Telegram'daki profil resminizi yanıtladığınız resimle değişir. """
    replymsg = await propic.get_reply_message()
    photo = None
    if replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await propic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await propic.client.download_file(replymsg.media.document)
        else:
            await propic.edit(INVALID_MEDIA)

    if photo:
        try:
            await propic.client(
                UploadProfilePhotoRequest(await
                                          propic.client.upload_file(photo)))
            os.remove(photo)
            await propic.edit(PP_CHANGED)
        except PhotoCropSizeSmallError:
            await propic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await propic.edit(PP_ERROR)
        except PhotoExtInvalidError:
            await propic.edit(INVALID_MEDIA)


@register(outgoing=True, pattern="^.setbio (.*)")
async def set_biograph(setbio):
    """ .setbio komutu Telegram'da yeni bir biyografi ayarlamanızı sağlar. """
    newbio = setbio.pattern_match.group(1)
    await setbio.client(UpdateProfileRequest(about=newbio))
    await setbio.edit(BIO_SUCCESS)


@register(outgoing=True, pattern="^.username (.*)")
async def update_username(username):
    """ .username komutu Telegram'da yeni bir kullanıcı adı belirlemenizi sağlar. """
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await username.edit(USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await username.edit(USERNAME_TAKEN)


@register(outgoing=True, pattern="^.count$")
async def count(event):
    """ .count komutu profil istatistiklerini gösterir. """
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    await event.edit("`Lütfen bekleyin..`")
    dialogs = await bot.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            print(d)

    result += f"`Kullanıcılar:`\t**{u}**\n"
    result += f"`Gruplar:`\t**{g}**\n"
    result += f"`Süpergruplar:`\t**{c}**\n"
    result += f"`Kanallar:`\t**{bc}**\n"
    result += f"`Botlar:`\t**{b}**"

    await event.edit(result)


@register(outgoing=True, pattern=r"^.delpfp")
async def remove_profilepic(delpfp):
    """ .delpfp komutu Telegram'daki şu anki profil resminizi kaldırır. """
    group = delpfp.text[8:]
    if group == 'all':
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1

    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.from_id,
                             offset=0,
                             max_id=0,
                             limit=lim))
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(
            InputPhoto(id=sep.id,
                       access_hash=sep.access_hash,
                       file_reference=sep.file_reference))
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await delpfp.edit(
        f"`{len(input_photos)} adet profil fotoğrafı silindi.`")


CMD_HELP.update({
    "profile":
    ".username <yeni kullanıcı adı>\
\nKullanımı: Telegram'daki kullanıcı adınızı değişir.\
\n\n.name <isim> or .name <isim> <soyisim>\
\nKullanımı: Telegram'daki isminizi değişir. (Ad ve soyad ilk boşluğa dayanarak birleştirilir.)\
\n\n.setpfp\
\nKullanımı: Bir resmi Telegram'da profil resmi yapmak için .setpfp komutuyla cevap verin.\
\n\n.setbio <yeni biyografi>\
\nKullanımı: Telegram'daki biyografinizi bu komutu kullanarak değiştirin..\
\n\n.delpfp or .delpfp <numara>/<all>\
\nKullanımı: Telegram profil fotoğrafınızı kaldırır.\
\n\n.reserved\
\nKullanımı: Rezerve ettiğiniz kullanıcı adlarını gösterir.\
\n\n.count\
\nKullanımı: Gruplarınızı, sohbetlerinizi, aktif botları vs. sayar."
})
