# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Küresel notlar tutmak için yapılmış olan UserBot modülü. """

from userbot.events import register
from userbot import CMD_HELP, BOTLOG_CHATID


@register(outgoing=True,
          pattern=r"\$\w*",
          ignore_unsafe=True,
          disable_errors=True)
async def on_snip(event):
    """ Snip mantığı. """
    try:
        from userbot.modules.sql_helper.snips_sql import get_snip
    except AttributeError:
        return
    name = event.text[1:]
    snip = get_snip(name)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if snip and snip.f_mesg_id:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(snip.f_mesg_id))
        await event.client.send_message(event.chat_id,
                                        msg_o.message,
                                        reply_to=message_id_to_reply,
                                        file=msg_o.media)
    elif snip and snip.reply:
        await event.client.send_message(event.chat_id,
                                        snip.reply,
                                        reply_to=message_id_to_reply)


@register(outgoing=True, pattern="^.snip (\w*)")
async def on_snip_save(event):
    """ .snip komutu gelecekte kullanılmak üzere snips kaydeder. """
    try:
        from userbot.modules.sql_helper.snips_sql import add_snip
    except AtrributeError:
        await event.edit("`SQL dışı modda çalışıyor!`")
        return
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#SNIP\
            \nKELIME: {keyword}\
            \n\nAşağıdaki mesaj snip için veri olarak kaydedilir, lütfen silmeyin !!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Snip'leri medya ile kaydetmek için BOTLOG_CHATID ayarlanması gerekir.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Snip {}. Kullanım:` **${}** `"
    if add_snip(keyword, string, msg_id) is False:
        await event.edit(success.format('güncellendi', keyword))
    else:
        await event.edit(success.format('kaydedildi', keyword))


@register(outgoing=True, pattern="^.snips$")
async def on_snip_list(event):
    """ .snips komutu sizin tarafınızdan kaydedilen snip'leri listeler. """
    try:
        from userbot.modules.sql_helper.snips_sql import get_snips
    except AttributeError:
        await event.edit("`SQL dışı modda çalışıyor!`")
        return

    message = "`Şu anda hiçbir snip mevcut değil.`"
    all_snips = get_snips()
    for a_snip in all_snips:
        if message == "`Şu anda hiçbir snip mevcut değil.`":
            message = "Mevcut snipler:\n"
            message += f"`${a_snip.snip}`\n"
        else:
            message += f"`${a_snip.snip}`\n"

    await event.edit(message)


@register(outgoing=True, pattern="^.remsnip (\w*)")
async def on_snip_delete(event):
    """ .remsnip komutu belirlenini snipi siler. """
    try:
        from userbot.modules.sql_helper.snips_sql import remove_snip
    except AttributeError:
        await event.edit("`SQL dışı modda çalışıyor!`")
        return
    name = event.pattern_match.group(1)
    if remove_snip(name) is True:
        await event.edit(f"`snip:` **{name}** `Başarıyla silindi`")
    else:
        await event.edit(f"`snip:` **{name}** `Bulunamadı` ")


CMD_HELP.update({
    "snips":
    "\
$<snip_adı>\
\nKullanım: Belirtilen snipi kullanır.\
\n\n.snip <isim> <veri> veya .snip <isim> ile bir iletiyi yanıtlayın.\
\nKullanım: Bir snip (küresel not) olarak kaydeder. (Resimler, dokümanlar ve çıkartmalar ile çalışır !)\
\n\n.snips\
\nKullanım: Kaydedilen tüm snip'leri listeler.\
\n\n.remsnip <snip_adı>\
\nKullanım: Belirtilen snip'i siler.\
"
})
