# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


from userbot.events import register
from userbot import CMD_HELP, bot, LOGS, CLEAN_WELCOME, BOTLOG_CHATID
from telethon.events import ChatAction


@bot.on(ChatAction)
async def welcome_to_chat(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import get_current_welcome_settings
        from userbot.modules.sql_helper.welcome_sql import update_previous_welcome
    except:
        return
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        """user_added=True,
        user_joined=True,
        user_left=False,
        user_kicked=False"""
        if (event.user_joined
                or event.user_added) and not (await event.get_user()).bot:
            if CLEAN_WELCOME:
                try:
                    await event.client.delete_messages(event.chat_id,
                                                       cws.previous_welcome)
                except Exception as e:
                    LOGS.warn(str(e))
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await event.client.get_me()

            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name,
                                                     a_user.id)
            my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = f"@{a_user.username}" if a_user.username else mention
            userid = a_user.id
            my_first = me.first_name
            my_last = me.last_name
            if my_last:
                my_fullname = f"{my_first} {my_last}"
            else:
                my_fullname = my_first
            my_username = f"@{me.username}" if me.username else my_mention
            file_media = None
            current_saved_welcome_message = None
            if cws and cws.f_mesg_id:
                msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                        ids=int(cws.f_mesg_id))
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
            elif cws and cws.reply:
                current_saved_welcome_message = cws.reply
            current_message = await event.reply(
                current_saved_welcome_message.format(mention=mention,
                                                     title=title,
                                                     count=count,
                                                     first=first,
                                                     last=last,
                                                     fullname=fullname,
                                                     username=username,
                                                     userid=userid,
                                                     my_first=my_first,
                                                     my_last=my_last,
                                                     my_fullname=my_fullname,
                                                     my_username=my_username,
                                                     my_mention=my_mention),
                file=file_media)
            update_previous_welcome(event.chat_id, current_message.id)


@register(outgoing=True, pattern=r"^.setwelcome(?: |$)(.*)")
async def save_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import add_welcome_setting
    except:
        await event.edit("`SQL dışı modda çalışıyor!`")
        return
    msg = await event.get_reply_message()
    string = event.pattern_match.group(1)
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#KARSILAMA_NOTU\
            \nGRUP ID: {event.chat_id}\
            \nAşağıdaki mesaj sohbet için yeni Karşılama notu olarak kaydedildi, lütfen silmeyin !!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Karşılama notunu kaydetmek için BOTLOG_CHATID ayarlanması gerekir.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Karşılama mesajı bu sohbet için {} `"
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        await event.edit(success.format('kaydedildi'))
    else:
        await event.edit(success.format('güncellendi'))


@register(outgoing=True, pattern="^.checkwelcome$")
async def show_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import get_current_welcome_settings
    except:
        await event.edit("`SQL dışı modda çalışıyor!`")
        return
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
        await event.edit("`Burada kayıtlı karşılama mesajı yok.`")
        return
    elif cws and cws.f_mesg_id:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(cws.f_mesg_id))
        await event.edit(
            "`Şu anda bu karşılama notu ile yeni kullanıcıları ağırlıyorum.`")
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws and cws.reply:
        await event.edit(
            "`Şu anda bu karşılama notu ile yeni kullanıcıları ağırlıyorum.`")
        await event.reply(cws.reply)


@register(outgoing=True, pattern="^.rmwelcome$")
async def del_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import rm_welcome_setting
    except:
        await event.edit("`SQL dışı modda çalışıyor!`")
        return
    if rm_welcome_setting(event.chat_id) is True:
        await event.edit("`Karşılama mesajı bu sohbet için silindi.`")
    else:
        await event.edit("`Burada karşılama notu var mı ?`")


CMD_HELP.update({
    "welcome":
    "\
.setwelcome <karışlama mesajı> veya .setwelcome ile bir mesaja cevap verin\
\nKullanım: Mesajı sohbete karşılama notu olarak kaydeder.\
\n\nKarşılama mesajlarını biçimlendirmek için kullanılabilir değişkenler :\
\n`{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`\
\n\n.checkwelcome\
\nKullanım: Sohbette karşılama notu olup olmadığını kontrol edin.\
\n\n.rmwelcome\
\nKullanım: Geçerli sohbet için karşılama notunu siler.\
"
})
