# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta
#

"""
Grup yönetmenize yardımcı olacak UserBot modülü
"""

from asyncio import sleep
from os import remove

from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest, InviteToChannelRequest)
from telethon.tl.functions.messages import (UpdatePinnedMessageRequest, AddChatUserRequest)
from telethon.tl.types import (PeerChannel, ChannelParticipantsAdmins,
                               ChatAdminRights, ChatBannedRights,
                               MessageEntityMentionName, MessageMediaPhoto,
                               ChannelParticipantsBots, User, InputPeerChat)
from telethon.events import ChatAction
from userbot import BOTLOG, BOTLOG_CHATID, BRAIN_CHECKER, CMD_HELP, bot, WARN_MODE, WARN_LIMIT, WHITELIST
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from userbot.cmdhelp import CmdHelp
import datetime

# =================== CONSTANT ===================
# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("admin")

# ████████████████████████████████ #

PP_TOO_SMOL = LANG['PP_TOO_SMOL']
PP_ERROR = LANG['PP_ERROR']
NO_ADMIN = LANG['NO_ADMIN']
NO_PERM = LANG['NO_PERM']
NO_SQL = LANG['NO_SQL']

CHAT_PP_CHANGED = LANG['CHAT_PP_CHANGED']
CHAT_PP_ERROR = LANG['CHAT_PP_ERROR']
INVALID_MEDIA = LANG['INVALID_MEDIA']

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================
@register(outgoing=True, groups_only = True, pattern="^.ekle ?(.*)")
async def ekle(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit(LANG['EKLE_PRIVATE'])
    else:
        if not event.is_channel and event.is_group:
            for user_id in to_add_users.split(" "):
                await event.edit(f'`{user_id} gruba ekleniyor...`')
                try:
                    await event.client(AddChatUserRequest(
                        chat_id=event.chat_id,
                        user_id=user_id,
                        fwd_limit=1000000
                    ))
                except Exception as e:
                    await event.edit(f'`{user_id} gruba eklenemedi!`')
                    continue
                await event.edit(f'`{user_id} gruba eklendi!`')
        else:
            for user_id in to_add_users.split(" "):
                await event.edit(f'`{user_id} gruba ekleniyor...`')
                try:
                    await event.client(InviteToChannelRequest(
                        channel=event.chat_id,
                        users=[user_id]
                    ))
                except Exception as e:
                    await event.edit(f'`{user_id} gruba eklenemedi!`')
                    continue
                await event.edit(f'`{user_id} gruba eklendi!`')

@register(outgoing=True, groups_only = True, pattern="^.gban(?: |$)(.*)")
async def gbanspider(gspdr):
    """ .gban komutu belirlenen kişiyi küresel olarak yasaklar """
    # Yetki kontrolü
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await gspdr.edit(LANG['BRAIN'])
        return

    # Başarı olursa bilgi ver
    await gspdr.edit(LANG['BANNING'])
    if gban(user.id) == False:
        await gspdr.edit(
            LANG['ALREADY_GBANNED'])
    else:
        if reason:
            await gspdr.edit(f"{LANG['GBANNED_REASON']} {reason}")
        else:
            await gspdr.edit(LANG['GBANNED'])

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)")


@register(incoming=True)
async def gbanmsg(moot):
    """ Küresel banlanan kullanıcı mesaj gelirse """
    try:
        from userbot.modules.sql_helper.gban_sql import is_gbanned
    except:
        return

    gbanned = is_gbanned(str(moot.sender_id))
    if gbanned == str(moot.sender_id):
        try:
            chat = await moot.get_chat()
        except:
            return
            
        if (type(chat) == User):
            return 

        admin = chat.admin_rights
        creator = chat.creator

        if not admin and not creator:
            return

        try:
            await moot.client(EditBannedRequest(moot.chat_id, moot.sender_id,
                                            BANNED_RIGHTS))
            await moot.reply(LANG['GBAN_TEXT'])
        except:
            return

@register(outgoing=True, groups_only = True, pattern="^.ungban(?: |$)(.*)")
async def ungban(un_gban):
    """ .ungban komutu belirlenen kişinin küresel susturulmasını kaldırır """
    # Yetki kontrolü
    chat = await un_gban.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await un_gban.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        from userbot.modules.sql_helper.gban_sql import ungban
    except:
        await un_gban.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gban)
    user = user[0]
    if user:
        pass
    else:
        return

    await un_gban.edit(LANG['UNGBANNING'])

    if ungban(user.id) is False:
        await un_gban.edit(LANG['NO_BANNED'])
    else:
        # Başarı olursa bilgi ver
        await un_gban.edit(LANG['UNGBANNED'])

        if BOTLOG:
            await un_gban.client.send_message(
                BOTLOG_CHATID, "#UNGBAN\n"
                f"KULLANICI: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {un_gban.chat.title}(`{un_gban.chat_id}`)")


@register(outgoing=True, pattern="^.setgpic$")
async def set_group_photo(gpic):
    """ .setgpic komutu ile grubunuzun fotoğrafını değiştirebilirsiniz """
    if not gpic.is_group:
        await gpic.edit(LANG['PRIVATE'])
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await
                                 gpic.client.upload_file(photo)))
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


@register(outgoing=True, groups_only = True, pattern="^.promote(?: |$)(.*)")
async def promote(promt):
    """ .promote komutu ile belirlenen kişiyi yönetici yapar """
    # Hedef sohbeti almak
    chat = await promt.get_chat()
    # Yetkiyi sorgula
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değilse geri dön
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(add_admins=True,
                                 invite_users=True,
                                 change_info=True,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)

    await promt.edit(LANG['PROMOTING'])
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "Yönetici"  # Her ihtimale karşı.
    if user:
        pass
    else:
        return

    # Geçerli kullanıcı yönetici veya sahip ise tanıtmaya çalışalım
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit(LANG['SUCCESS_PROMOTE'])

    # Telethon BadRequestError hatası verirse
    # yönetici yapma yetkimiz yoktur
    except:
        await promt.edit(NO_PERM)
        return

    # Yetkilendirme işi başarılı olursa günlüğe belirtelim
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#YETKI\n"
            f"KULLANICI: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {promt.chat.title}(`{promt.chat_id}`)")


@register(outgoing=True, groups_only = True, pattern="^.demote(?: |$)(.*)")
async def demote(dmod):
    """ .demote komutu belirlenen kişiyi yöneticilikten çıkarır """
    # Yetki kontrolü
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # Eğer başarılı olursa, yetki düşürüleceğini beyan edelim
    await dmod.edit(LANG['UNPROMOTING'])
    rank = "admeme"  # Burayı öylesine yazdım
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    # Yetki düşürme sonrası yeni izinler
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    # Yönetici iznini düzenle
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # Telethon BadRequestError hatası verirse
    # gerekli yetkimiz yoktur
    except:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit(LANG['UNPROMOTE'])

    # Yetki düşürme işi başarılı olursa günlüğe belirtelim
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#YETKIDUSURME\n"
            f"KULLANICI: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {dmod.chat.title}(`{dmod.chat_id}`)")


@register(outgoing=True, groups_only = True, pattern="^.ban(?: |$)(.*)")
async def ban(bon):
    """ .ban komutu belirlenen kişiyi gruptan yasaklar """
    # Yetki kontrolü
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await bon.edit(
            LANG['BRAIN']
        )
        return

    # Hedefi yasaklayacağınızı duyurun
    await bon.edit(LANG['BANNING'])

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except:
        await bon.edit(NO_PERM)
        return
    # Spamcılar için
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except:
        await bon.edit(
            LANG['NO_PERM_BUT_BANNED'])
        return
    # Mesajı silin ve ardından komutun
    # incelikle yapıldığını söyleyin
    SONMESAJ = PLUGIN_MESAJLAR['ban'].format(
        id = user.id,
        username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
        first_name = user.first_name,
        last_name = '' if not user.last_name else user.last_name,
        mention = f"[{user.first_name}](tg://user?id={user.id})",
        date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
        count = (chat.participants_count - 1) if chat.participants_count else 'Bilinmiyor'
    )
    
    if reason:
        await bon.edit(f"{SONMESAJ}\n{LANG['REASON']}: {reason}")
    else:
        await bon.edit(SONMESAJ)
    # Yasaklama işlemini günlüğe belirtelim
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID, "#BAN\n"
            f"KULLANICI: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {bon.chat.title}(`{bon.chat_id}`)")


@register(outgoing=True, groups_only = True, pattern="^.unban(?: |$)(.*)")
async def nothanos(unbon):
    """ .unban komutu belirlenen kişinin yasağını kaldırır """
    # Yetki kontrolü
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    # Her şey yolunda giderse...
    await unbon.edit(LANG['UNBANNING'])

    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit(LANG['UNBANNED'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmiyor'
        ))

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID, "#UNBAN\n"
                f"KULLANICI: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {unbon.chat.title}(`{unbon.chat_id}`)")
    except:
        await unbon.edit(LANG['EXCUSE_ME_WTF'])


@register(outgoing=True, groups_only = True, pattern="^.mute(?: |$)(.*)")
async def spider(spdr):
    """
    Bu fonksiyon temelde susturmaya yarar
    """
    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except:
        await spdr.edit(NO_SQL)
        return

    # Yetki kontrolü
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await spdr.edit(
            LANG['BRAIN']
        )
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        await spdr.edit(
            LANG['NO_MUTE_ME'])
        return

    # Hedefi sustaracağınızı duyurun
    await spdr.edit(LANG['MUTING'])
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit(LANG['ALREADY_MUTED'])
    else:
        try:
            await spdr.client(
                EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            await mutmsg(spdr, user, reason, chat)
        except UserAdminInvalidError:
            await mutmsg(spdr, user, reason, chat)
        except:
            return await spdr.edit(LANG['WTF_MUTE'])


async def mutmsg(spdr, user, reason, chat):
    # Fonksiyonun yapıldığını duyurun
    SONMESAJ = PLUGIN_MESAJLAR['mute'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmiyor'
        )

    if reason:
        await spdr.edit(f"{SONMESAJ}\n{LANG['REASON']}: {reason}")
    else:
        await spdr.edit(f"{SONMESAJ}")

    # Susturma işlemini günlüğe belirtelim
    if BOTLOG:
        await spdr.client.send_message(
            BOTLOG_CHATID, "#MUTE\n"
            f"KULLANICI: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {spdr.chat.title}(`{spdr.chat_id}`)")


@register(outgoing=True, groups_only = True, pattern="^.unmute(?: |$)(.*)")
async def unmoot(unmot):
    """ .unmute komutu belirlenin kişinin sesini açar (yani grupta tekrardan konuşabilir) """
    # Yetki kontrolü
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except:
        await unmot.edit(NO_SQL)
        return

    await unmot.edit(LANG['UNMUTING'])
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit(LANG['ALREADY_UNMUTED'])
    else:

        try:
            await unmot.client(
                EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit(LANG['UNMUTED'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmiyor'
        ))
        except UserAdminInvalidError:
            await unmot.edit(LANG['UNMUTED'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmiyor'
        ))
        except:
            await unmot.edit(LANG['WTF_MUTE'])
            return

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID, "#UNMUTE\n"
                f"KULLANICI: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {unmot.chat.title}(`{unmot.chat_id}`)")


@register(incoming=True)
async def muter(moot):
    """ Sessize alınan kullanıcıların mesajlarını silmek için kullanılır """
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                try:
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id, rights))
                except:
                    pass
    if gmuted:
        for i in gmuted:
            if i.sender == str(moot.sender_id):
                await moot.delete()

@register(outgoing=True, groups_only = True, pattern="^.ungmute(?: |$)(.*)")
async def ungmoot(un_gmute):
    """ .ungmute komutu belirlenen kişinin küresel susturulmasını kaldırır """
    # Yetki kontrolü
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await un_gmute.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        from userbot.modules.sql_helper.gmute_sql import ungmute
    except:
        await un_gmute.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if user:
        pass
    else:
        return

    await un_gmute.edit(LANG['GUNMUTING'])

    if ungmute(user.id) is False:
        await un_gmute.edit(LANG['NO_GMUTE'])
    else:
        # Başarı olursa bilgi ver
        await un_gmute.edit(LANG['UNMUTED'])

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID, "#UNGMUTE\n"
                f"KULLANICI: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {un_gmute.chat.title}(`{un_gmute.chat_id}`)")


@register(outgoing=True, groups_only = True, pattern="^.gmute(?: |$)(.*)")
async def gspider(gspdr):
    """ .gmute komutu belirlenen kişiyi küresel olarak susturur """
    # Yetki kontrolü
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await gspdr.edit(LANG['BRAIN'])
        return

    # Başarı olursa bilgi ver
    await gspdr.edit(LANG['GMUTING'])
    if gmute(user.id) == False:
        await gspdr.edit(
            LANG['ALREADY_GMUTED'])
    else:
        if reason:
            await gspdr.edit(f"{LANG['GMUTED']} {LANG['REASON']}: {reason}")
        else:
            await gspdr.edit(LANG['GMUTED'])

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)")


@register(outgoing=True, pattern="^.zombies(?: |$)(.*)", groups_only = False)
async def rm_deletedacc(show):
    """ .zombies komutu bir sohbette tüm hayalet / silinmiş / zombi hesaplarını listeler. """

    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = LANG['NO_ZOMBIE']

    if con != "clean":
        await show.edit(LANG['ZOMBIE'])
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = LANG['ZOMBIES'].format(del_u)
        await show.edit(del_status)
        return

    # Yetki kontrolü
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await show.edit(LANG['NO_ADMIN'])
        return

    await show.edit(LANG['CLEANING'])
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            except:
                await show.edit(LANG['NO_BAN_YT'])
                return
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"**{del_u}** {LANG['DELETED']}"

    if del_a > 0:
        del_status = f"**{del_u}** {LANG['DELETED']} \
        \n**{del_a}** tane silinmiş olan yönetici hesapları çıkartılamadı"

    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID, "#TEMIZLIK\n"
            f"**{del_u}** tane silinmiş hesap çıkartıldı !!\
            \nGRUP: {show.chat.title}(`{show.chat_id}`)")


@register(outgoing=True, groups_only = True, pattern="^.admins$")
async def get_admin(show):
    """ .admins komutu girilen gruba ait yöneticileri listeler """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b>{title} {LANG["ADMINS"]}:</b> \n'
    try:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsAdmins):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nDeleted Account <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@register(outgoing=True, pattern="^.pin(?: |$)(.*)")
async def pin(msg):
    """ .pin komutu verildiği grupta ki yazıyı & medyayı sabitler """
    # Yönetici kontrolü
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit(LANG['NEED_MSG'])
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except:
        await msg.edit(NO_PERM)
        return

    await msg.edit(LANG['PINNED'])

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}")


@register(outgoing=True, groups_only = True, pattern="^.kick(?: |$)(.*)")
async def kick(usr):
    """ .kick komutu belirlenen kişiyi gruptan çıkartır """
    # Yetki kontrolü
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return
    try:
        user, reason = await get_user_from_event(usr)
    except TypeError:
        user = False # Boş kaldığı zaman hata logu oluşturmaması için

    if not user:
        await usr.edit(LANG['NOT_FOUND'])
        return

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await usr.edit(
            LANG['BRAIN']
        )
        return

    await usr.edit(LANG['KICKING'])

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `{LANG['KICKED']}`\n{LANG['REASON']}: {reason}"
        )
    else:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `{LANG['KICKED']}`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#KICK\n"
            f"KULLANICI: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {usr.chat.title}(`{usr.chat_id}`)\n")


@register(outgoing=True, groups_only = True, pattern="^.users ?(.*)")
async def get_users(show):
    """ .users komutu girilen gruba ait kişileri listeler """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '{} grubunda bulunan kişiler: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nSilinen hesap `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nSilinen hesap `{user.id}`"
    except Exception as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Lanet olsun, bu büyük bir grup. Kullanıcı listesini dosya olarak gönderiyorum.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption='{} grubundaki kişiler'.format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """ Kullanıcıyı argümandan veya yanıtlanan mesajdan alın. """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Kişinin kullanıcı adını, ID'sini veya yanıtını iletin!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except Exception as err:
        await event.edit(str(err))
        return None

    return user_obj

@register(outgoing=True, groups_only = True, pattern="^.unwarn ?(.*)")
async def unwarn(event):
    """ .unwarn kullanıcıyı uyarıyı kaldırmaya işe yarar """
    # Yetki kontrolü
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await event.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        import userbot.modules.sql_helper.warn_sql as warn
    except:
        await event.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    # Başarı olursa bilgi ver
    await event.edit(LANG['UNWARNING'])
    silme = warn.sil_warn(user.id)
    if silme == False:
        await event.edit(LANG['UNWARNED'])
        return

    warnsayi = warn.getir_warn(user.id)
    
    await event.edit(f"[{user.first_name}](tg://user?id={user.id})`, {LANG['UNWARN']} {warnsayi}/{WARN_LIMIT}`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#WARN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")

@register(outgoing=True, groups_only = True, pattern="^.warn ?(.*)")
async def warn(event):
    """ .warn kullanıcıyı uyarmaya işe yarar """
    # Yetki kontrolü
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Yönetici değil ise geri dön
    if not admin and not creator:
        await event.edit(NO_ADMIN)
        return

    # Fonksiyonun SQL modu altında çalışıp çalışmadığını kontrol et
    try:
        import userbot.modules.sql_helper.warn_sql as warn
    except:
        await event.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    # Eğer kullanıcı sudo ise
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await event.edit(LANG['BRAIN'])
        return

    # Başarı olursa bilgi ver
    await event.edit(LANG['WARNING'])
    warn.ekle_warn(user.id)
    warnsayi = warn.getir_warn(user.id)
    if warnsayi >= WARN_LIMIT:
        if WARN_MODE == "gban":
            await Warn_Gban(event, warn, user)
        else:
            await Warn_Gmute(event, warn, user)
        return
    await event.edit(f"[{user.first_name}](tg://user?id={user.id})`, {warnsayi}/{WARN_LIMIT} {LANG['WARN']}`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#WARN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")

async def Warn_Gmute(event, warn, user, reason = None):
    await event.delete()
    yeni = await event.reply(f"`Seni yeteri kadar uyardım` [{user.first_name}](tg://user?id={user.id})`, küresel olarak susturuldun!`")

    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except:
        await yeni.edit(NO_SQL)
        return
        
    yeni2 = await yeni.reply("`Susturuluyor...`")
        
    if gmute(user.id) == False:
        await yeni2.edit(
            '`Hata! Kullanıcı zaten küresel olarak susturuldu.`')
    else:
        if reason != None:
            await yeni2.edit(f"`Kullanıcı küresel olarak susturuldu!`Nedeni: {reason}")
        else:
            await yeni2.edit("`Kullanıcı küresel olarak susturuldu!`")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)")
    warn.toplu_sil_warn(user.id)

async def Warn_Gban(event, warn, user, reason = None):
    await event.delete()
    yeni = await event.reply(f"`Seni yeteri kadar uyardım` [{user.first_name}](tg://user?id={user.id})`, küresel olarak yasaklandıın!`")

    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except:
        await yeni.edit(NO_SQL)
        return
        
    yeni2 = await yeni.reply("`Yasaklanıyor...`")
        
    if gban(user.id) == False:
        await yeni2.edit(
            '`Hata! Kullanıcı zaten küresel olarak yasaklandı.`')
    else:
        if reason != None:
            await yeni2.edit(f"`Kullanıcı küresel olarak yasaklandı!`Nedeni: {reason}")
        else:
            await yeni2.edit("`Kullanıcı küresel olarak yasaklandı!`")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#GBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)")
    warn.toplu_sil_warn(user.id)

@register(outgoing=True, groups_only = True, pattern="^.usersdel ?(.*)")
async def get_usersdel(show):
    """ .usersdel komutu grup içinde ki silinen hesapları gösterir """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '{} grubunda bulunan silinmiş hesaplar: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
         #       else:
    #                mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
         #       else:
      #              mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Lanet olsun, bu büyük bir grup. Silinen kullanıcılar listesini dosya olarak gönderiyorum.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "deleteduserslist.txt",
            caption='{} grubuna ait olan silinmiş hesaplar:'.format(title),
            reply_to=show.id,
        )
        remove("deleteduserslist.txt")


async def get_userdel_from_event(event):
    """ Silinen kullanıcıyı argümandan veya yanıtlanan mesajdan alın. """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Silinen kullanıcının kullanıcı adını, ID'sini veya yanıtını iletin!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_userdel_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except Exception as err:
        await event.edit(str(err))
        return None

    return user_obj


@register(outgoing=True, pattern="^.bots$", groups_only =True)
async def get_bots(show):
    """ .bots komutu gruba ait olan botları listeler """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b> {title} grubunda bulunan botlar:</b>\n'
    try:
       # if isinstance(message.to_id, PeerChat):
        #    await show.edit("`Sadece süper grupların botlara sahip olabileceğini duydum.`")
        #   return
       # else:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsBots):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nSilinmiş bot <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await show.edit(
            "Lanet olsun, burada çok fazla bot var. Botların listesini dosya olarak gönderiyorum.")
        file = open("botlist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "botlist.txt",
            caption='{} grubunda bulunan botlar:'.format(title),
            reply_to=show.id,
        )
        remove("botlist.txt")

CmdHelp('admin').add_command(
        'promote', '<kullanıcı adı/yanıtlama> <özel isim (isteğe bağlı)>', 'Sohbetteki kişiye yönetici hakları sağlar.'
    ).add_command(
        'demote', '<kullanıcı adı/yanıtlama>', 'Sohbetteki kişinin yönetici izinlerini iptal eder.'
    ).add_command(
        'ban', '<kullanıcı adı/yanıtlama> <nedeni (isteğe bağlı)>', 'Sohbetteki kişiyi susturur, yöneticilerde de çalışır.'
    ).add_command(
        'unban', '<kullanıcı adı/yanıtlama>', 'Sohbetteki kişinin yasağını kaldırır.'
    ).add_command(
        'kick', '<kullanıcı adı/yanıtlama> <nedeni (isteğe bağlı)>', 'Gruptan belirttiğiniz kişiyi tekmeler.'
    ).add_command(
        'gmute', '<kullanıcı adı/yanıtlama> <nedeni (isteğe bağlı)>', 'Kişiyi yönetici olduğunuz tüm gruplarda susturur.'
    ).add_command(
        'ungmute', '<kullanıcı adı/yanıtlama>', 'Kişiyi küresel olarak sessize alınanlar listesinden kaldırır.'
    ).add_command(
        'zombies', None, 'Bir gruptaki silinmiş hesapları arar. Gruptan silinen hesapları kaldırmak için .zombies clean komutunu kullanın.'
    ).add_command(
        'admins', None, 'Sohbet yöneticilerinin listesini alır.'
    ).add_command(
        'bots', None, 'Bir gruptaki silinmiş hesapları arar. Gruptan silinen hesapları kaldırmak için .zombies clean komutunu kullanın.'
    ).add_command(
        'users veya .users', '<kullanıcı adı> <kullanıcı adı/yanıtlama>', 'Sohbetteki tüm (veya sorgulanan) kullanıcıları alır.'
    ).add_command(
        'setgppic', '<yanıtlanan resim>', 'Grubun resmini değiştirir.'
    ).add_command(
        'warn', '<kullanıcı adı/yanıtlamma> <sebep (isteğe bağlı>', 'Belirttiğiniz kullanıcıyı uyarır.'
    ).add_command(
        'unwarn', '<kullanıcı adı/yanıtlamma> <sebep (isteğe bağlı>', 'Belirttiğiniz kullanıcının uyarısını kaldırır.'
    ).add_command(
        'warn', '<kullanıcı adı/yanıtlamma> <sebep (isteğe bağlı>', 'Belirttiğiniz kullanıcıyı uyarır.'
    ).add_command(
        'usersdel', None, 'Grup içerisinde silinen hesapları göstürür.'
    ).add_command(
        'ekle', '<kullanıcı ad(lar)ı>', 'Gruba üye ekler.'
    ).add_command(
        'gban', '<kullanıcı adı/yanıtlama>', 'Kullanıcıyı küresel olarak yasaklar.'
    ).add_command(
        'ungban', '<kullanıcı adı/yanıtlama>', 'Kullanıcının küresel yasaklamasını kaldırır.'
    ).add_command(
        'pin', '<yanıtlama>', 'Yanıt verdiğiniz mesajı başa sabitler.'
    ).add_command(
        'setgpic', '<yanıtlama>', 'Grup fotoğrafını değiştirir.'
    ).add()
