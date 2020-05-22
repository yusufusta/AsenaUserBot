# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Filtre komutlarını içeren UserBot modülüdür. """

from asyncio import sleep
import re
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(incoming=True, disable_edited=True, disable_errors=True)
async def filter_incoming_handler(handler):
    """ Gelen mesajın filtre tetikleyicisi içerip içermediğini kontrol eder """
    try:
        if not (await handler.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.filter_sql import get_filters
            except AttributeError:
                await handler.edit("`Bot Non-SQL modunda çalışıyor!!`")
                return
            name = handler.raw_text
            filters = get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pro = re.fullmatch(trigger.keyword, name, flags=re.IGNORECASE)
                if pro and trigger.f_mesg_id:
                    msg_o = await handler.client.get_messages(
                        entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id))
                    await handler.reply(msg_o.message, file=msg_o.media)
                elif pro and trigger.reply:
                    await handler.reply(trigger.reply)
    except AttributeError:
        pass


@register(outgoing=True, pattern="^.filter (\w*)")
async def add_new_filter(new_handler):
    """ .filter komutu bir sohbete yeni filtreler eklemeye izin verir """
    try:
        from userbot.modules.sql_helper.filter_sql import add_filter
    except AttributeError:
        await new_handler.edit("`Bot Non-SQL modunda çalışıyor!!`")
        return
    mesj = new_handler.text

    if '"' in mesj:
        keyword = re.findall(r"\"(.*)\"", mesj)[0]
        string = re.findall(r"\s\S*$", mesj)[0]
    else:
        keyword = new_handler.pattern_match.group(1)
        string = new_handler.text.partition(keyword)[2]

    msg = await new_handler.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await new_handler.client.send_message(
                BOTLOG_CHATID, f"#FILTER\
            \nGrup ID: {new_handler.chat_id}\
            \nFiltre: {keyword}\
            \n\nBu mesaj filtrenin cevaplanması için kaydedildi, lütfen bu mesajı silmeyin!"
            )
            msg_o = await new_handler.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=new_handler.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await new_handler.edit(
                "`Bir medyanın filtreye karşılık olarak kaydedilebilmesi için BOTLOG_CHATID değerinin ayarlanması gerekli.`"
            )
            return
    elif new_handler.reply_to_msg_id and not string:
        rep_msg = await new_handler.get_reply_message()
        string = rep_msg.text
    success = " **{}** `filtresi {}`"
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        await new_handler.edit(success.format(keyword, 'eklendi'))
    else:
        await new_handler.edit(success.format(keyword, 'güncellendi'))


@register(outgoing=True, pattern="^.stop (\w*)")
async def remove_a_filter(r_handler):
    """ .stop komutu bir filtreyi durdurmanızı sağlar. """
    try:
        from userbot.modules.sql_helper.filter_sql import remove_filter
    except AttributeError:
        await r_handler.edit("`Bot Non-SQL modunda çalışıyor!!`")
        return
    filt = r_handler.pattern_match.group(1)
    if not remove_filter(r_handler.chat_id, filt):
        await r_handler.edit(" **{}** `filtresi mevcut değil.`".format(filt))
    else:
        await r_handler.edit(
            "**{}** `filtresi başarıyla silindi`".format(filt))


@register(outgoing=True, pattern="^.rmbotfilters (.*)")
async def kick_marie_filter(event):
    """ .rmfilters komutu Marie'de (ya da onun tabanındaki botlarda) \
        kayıtlı olan notları silmeye yarar. """
    cmd = event.text[0]
    bot_type = event.pattern_match.group(1).lower()
    if bot_type not in ["marie", "rose"]:
        await event.edit("`Bu bot henüz desteklenmiyor.`")
        return
    await event.edit("```Tüm filtreler temizleniyor...```")
    await sleep(3)
    resp = await event.get_reply_message()
    filters = resp.text.split("-")[1:]
    for i in filters:
        if bot_type.lower() == "marie":
            await event.reply("/stop %s" % (i.strip()))
        if bot_type.lower() == "rose":
            i = i.replace('`', '')
            await event.reply("/stop %s" % (i.strip()))
        await sleep(0.3)
    await event.respond(
        "```Botlardaki filtreler başarıyla temizlendi.```")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "Şu sohbetteki tüm filtreleri temizledim: " + str(event.chat_id))


@register(outgoing=True, pattern="^.filters$")
async def filters_active(event):
    """ .filters komutu bir sohbetteki tüm aktif filtreleri gösterir. """
    try:
        from userbot.modules.sql_helper.filter_sql import get_filters
    except AttributeError:
        await event.edit("`Bot Non-SQL modunda çalışıyor!!`")
        return
    transact = "`Bu sohbette hiç filtre yok.`"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if transact == "`Bu sohbette hiç filtre yok.`":
            transact = "Sohbetteki filtreler:\n"
            transact += "`{}`\n".format(filt.keyword)
        else:
            transact += "`{}`\n".format(filt.keyword)

    await event.edit(transact)


CMD_HELP.update({
    "filter":
    ".filters\
    \nKullanım: Bir sohbetteki tüm userbot filtrelerini listeler.\
    \n\n.filter <filtrelenecek kelime> <cevaplanacak metin> ya da bir mesajı .filter <filtrelenecek kelime>\
    \nKullanım: 'filtrelenecek kelime' olarak istenilen şeyi kaydeder.\
    \nBot her 'filtrelenecek kelime' yi algıladığında o mesaja cevap verecektir.\
    \nDosyalardan çıkartmalara her türlü şeyle çalışır.\
    \n\n.stop <filtre>\
    \nKullanım: Seçilen filtreyi durdurur.\
    \n\n.rmbotfilters <marie/rose>\
    \nKullanım: Grup yönetimi botlarındaki tüm filtreleri temizler. (Şu anlık Rose, Marie ve Marie klonları destekleniyor.)"
})
