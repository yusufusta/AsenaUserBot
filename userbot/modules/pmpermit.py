# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Kimin size özel mesaj gönderebileceğini kontrol altına almanızı sağlayan UserBot modülüdür. """

from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.types import User
from sqlalchemy.exc import IntegrityError

from userbot import (COUNT_PM, CMD_HELP, BOTLOG, BOTLOG_CHATID,
                     PM_AUTO_BAN, LASTMSG, LOGS)
from userbot.events import register

# ========================= CONSTANTS ============================
UNAPPROVED_MSG = ("`Hey! Bu bir bot. Endişelenme.\n\n`"
                  "`Sahibim sana PM atma izni vermedi. `"
                  "`Lütfen sahibimin aktif olmasını bekleyin, o genellikle PM'leri onaylar.\n\n`"
                  "`Bildiğim kadarıyla o kafayı yemiş insanlara PM izni vermiyor.`")
# =================================================================


@register(incoming=True, disable_edited=True, disable_errors=True)
async def permitpm(event):
    """ İzniniz olmadan size PM gönderenleri yasaklamak içindir. \
        Yazmaya devam eden kullanıcıları engeller. """
    if PM_AUTO_BAN:
        self_user = await event.client.get_me()
        if event.is_private and event.chat_id != 777000 and event.chat_id != self_user.id and not (
                await event.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                from userbot.modules.sql_helper.globals import gvarstatus
            except AttributeError:
                return
            apprv = is_approved(event.chat_id)
            notifsoff = gvarstatus("NOTIF_OFF")

            # Bu bölüm basitçe akıl sağlığı kontrolüdür.
            # Eğer mesaj daha önceden onaylanmamış olarak gönderildiyse
            # flood yapmayı önlemek için unapprove mesajı göndermeyi durdurur.
            if not apprv and event.text != UNAPPROVED_MSG:
                if event.chat_id in LASTMSG:
                    prevmsg = LASTMSG[event.chat_id]
                    # Eğer önceden gönderilmiş mesaj farklıysa unapprove mesajı tekrardan gönderilir.
                    if event.text != prevmsg:
                        async for message in event.client.iter_messages(
                                event.chat_id,
                                from_user='me',
                                search=UNAPPROVED_MSG):
                            await message.delete()
                        await event.reply(UNAPPROVED_MSG)
                    LASTMSG.update({event.chat_id: event.text})
                else:
                    await event.reply(UNAPPROVED_MSG)
                    LASTMSG.update({event.chat_id: event.text})

                if notifsoff:
                    await event.client.send_read_acknowledge(event.chat_id)
                if event.chat_id not in COUNT_PM:
                    COUNT_PM.update({event.chat_id: 1})
                else:
                    COUNT_PM[event.chat_id] = COUNT_PM[event.chat_id] + 1

                if COUNT_PM[event.chat_id] > 4:
                    await event.respond(
                        "`Sen benim sahibimin PM'ini spamlıyorsun, bu benim hoşuma gitmiyor.`\n"
                        "`Şu an ENGELLENDIN ve SPAM olarak bildirildin, ileride değişiklik olmadığı sürece..`"
                    )

                    try:
                        del COUNT_PM[event.chat_id]
                        del LASTMSG[event.chat_id]
                    except KeyError:
                        if BOTLOG:
                            await event.client.send_message(
                                BOTLOG_CHATID,
                                "PM sayacı kafayı yemiş gibi, botu lütfen yeniden başlatın.",
                            )
                        LOGS.info(
                            "PM sayacı kafayı yemiş gibi, botu lütfen yeniden başlatın.")
                        return

                    await event.client(BlockRequest(event.chat_id))
                    await event.client(ReportSpamRequest(peer=event.chat_id))

                    if BOTLOG:
                        name = await event.client.get_entity(event.chat_id)
                        name0 = str(name.first_name)
                        await event.client.send_message(
                            BOTLOG_CHATID,
                            "[" + name0 + "](tg://user?id=" +
                            str(event.chat_id) + ")" +
                            " kişisi sadece bir hayal kırıklığı idi. PM'ni meşgul ettiği için engellendi.",
                        )


@register(disable_edited=True, outgoing=True, disable_errors=True)
async def auto_accept(event):
    """ İlk mesajı atan sizseniz otomatik olarak onaylanır. """
    if not PM_AUTO_BAN:
        return
    self_user = await event.client.get_me()
    if event.is_private and event.chat_id != 777000 and event.chat_id != self_user.id and not (
            await event.get_sender()).bot:
        try:
            from userbot.modules.sql_helper.pm_permit_sql import is_approved
            from userbot.modules.sql_helper.pm_permit_sql import approve
        except AttributeError:
            return

        chat = await event.get_chat()
        if isinstance(chat, User):
            if is_approved(event.chat_id) or chat.bot:
                return
            async for message in event.client.iter_messages(event.chat_id,
                                                            reverse=True,
                                                            limit=1):
                if message.message is not UNAPPROVED_MSG and message.from_id == self_user.id:
                    try:
                        approve(event.chat_id)
                    except IntegrityError:
                        return

                if is_approved(event.chat_id) and BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#OTOMATIK-ONAYLANDI\n" + "Kullanıcı: " +
                        f"[{chat.first_name}](tg://user?id={chat.id})",
                    )


@register(outgoing=True, pattern="^.notifoff$")
async def notifoff(noff_event):
    """ .notifoff komutu onaylanmamış kişilerden gelen PM lerden bildirim almamanızı sağlar. """
    try:
        from userbot.modules.sql_helper.globals import addgvar
    except AttributeError:
        await noff_event.edit("`Bot Non-SQL modunda çalışıyor!!`")
        return
    addgvar("NOTIF_OFF", True)
    await noff_event.edit("`PM izni olmayan kullanıcıların bildirimleri sessize alındı!`")


@register(outgoing=True, pattern="^.notifon$")
async def notifon(non_event):
    """ .notifon komutu onaylanmamış kişilerden gelen PM lerden bildirim almanızı sağlar. """
    try:
        from userbot.modules.sql_helper.globals import delgvar
    except:
        await non_event.edit("`Bot Non-SQL modunda çalışıyor!!`")
        return
    delgvar("NOTIF_OFF")
    await non_event.edit("`PM izni olmayan kullanıcıarın bildirim göndermesine izin verildi!`")


@register(outgoing=True, pattern="^.approve$")
async def approvepm(apprvpm):
    """ .approve komutu herhangi birine PM atabilme izni verir. """
    try:
        from userbot.modules.sql_helper.pm_permit_sql import approve
    except:
        await apprvpm.edit("`Bot Non-SQL modunda çalışıyor!!`")
        return

    if apprvpm.reply_to_msg_id:
        reply = await apprvpm.get_reply_message()
        replied_user = await apprvpm.client.get_entity(reply.from_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id

    else:
        aname = await apprvpm.client.get_entity(apprvpm.chat_id)
        name0 = str(aname.first_name)
        uid = apprvpm.chat_id

    try:
        approve(uid)
    except IntegrityError:
        await apprvpm.edit("`Kullanıcı halihazırda PM gönderebiliyor olmalıdır.`")
        return

    await apprvpm.edit(f"[{name0}](tg://user?id={uid}) `kişisi PM gönderebilir!`")

    async for message in apprvpm.client.iter_messages(apprvpm.chat_id,
                                                      from_user='me',
                                                      search=UNAPPROVED_MSG):
        await message.delete()

    if BOTLOG:
        await apprvpm.client.send_message(
            BOTLOG_CHATID,
            "#ONAYLANDI\n" + "Kullanıcı: " + f"[{name0}](tg://user?id={uid})",
        )


@register(outgoing=True, pattern="^.disapprove$")
async def disapprovepm(disapprvpm):
    try:
        from userbot.modules.sql_helper.pm_permit_sql import dissprove
    except:
        await disapprvpm.edit("`Bot Non-SQL modunda çalışıyor!!`")
        return

    if disapprvpm.reply_to_msg_id:
        reply = await disapprvpm.get_reply_message()
        replied_user = await disapprvpm.client.get_entity(reply.from_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        dissprove(replied_user.id)
    else:
        dissprove(disapprvpm.chat_id)
        aname = await disapprvpm.client.get_entity(disapprvpm.chat_id)
        name0 = str(aname.first_name)

    await disapprvpm.edit(
        f"[{name0}](tg://user?id={disapprvpm.chat_id}) `kişisinin PM atma izni kaldırıldı.`")

    if BOTLOG:
        await disapprvpm.client.send_message(
            BOTLOG_CHATID,
            f"[{name0}](tg://user?id={disapprvpm.chat_id})"
            " kişisinin PM atma izni kaldırıldı.",
        )


@register(outgoing=True, pattern="^.block$")
async def blockpm(block):
    """ .block komutu insanları engellemenizi sağlar. """
    if block.reply_to_msg_id:
        reply = await block.get_reply_message()
        replied_user = await block.client.get_entity(reply.from_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        await block.client(BlockRequest(replied_user.id))
        await block.edit("`Engellendin!`")
        uid = replied_user.id
    else:
        await block.client(BlockRequest(block.chat_id))
        aname = await block.client.get_entity(block.chat_id)
        await block.edit("`Engellendin!`")
        name0 = str(aname.first_name)
        uid = block.chat_id

    try:
        from userbot.modules.sql_helper.pm_permit_sql import dissprove
        dissprove(uid)
    except:
        pass

    if BOTLOG:
        await block.client.send_message(
            BOTLOG_CHATID,
            "#ENGELLENDI\n" + "Kullanıcı: " + f"[{name0}](tg://user?id={uid})",
        )


@register(outgoing=True, pattern="^.unblock$")
async def unblockpm(unblock):
    """ .unblock komutu insanların size yeniden PM atabilmelerini sağlar. """
    if unblock.reply_to_msg_id:
        reply = await unblock.get_reply_message()
        replied_user = await unblock.client.get_entity(reply.from_id)
        name0 = str(replied_user.first_name)
        await unblock.client(UnblockRequest(replied_user.id))
        await unblock.edit("`Engelin kaldırıldı.`")

    if BOTLOG:
        await unblock.client.send_message(
            BOTLOG_CHATID,
            f"[{name0}](tg://user?id={replied_user.id})"
            " kişisinin engeli kaldırıldı.",
        )


CMD_HELP.update({
    "pmpermit":
    "\
.approve\
\nKullanım: Yanıt verilen kullanıcıya PM atma izni verilir.\
\n\n.disapprove\
\nKullanım: Yanıt verilen kullanıcının PM onayını kaldırır.\
\n\n.block\
\nKullanım: Bir kullanıcıyı engeller.1\
\n\n.unblock\
\nKullanımı: Engellenmiş kullanıcının engelini kaldırır.\
\n\n.notifoff\
\nKullanım: Onaylanmamış özel mesajların bildirimlerini temizler ya da devre dışı bırakır.\
\n\n.notifon\
\nKullanım: Onaylanmamış özel mesajların bildirim göndermesine izin verir."
})
