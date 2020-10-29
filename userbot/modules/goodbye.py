# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


from userbot.events import register
from userbot import CMD_HELP, bot, LOGS, CLEAN_WELCOME, BOTLOG_CHATID
from telethon.events import ChatAction
from userbot.cmdhelp import CmdHelp

@bot.on(ChatAction)
async def goodbye_to_chat(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import get_current_goodbye_settings
        from userbot.modules.sql_helper.goodbye_sql import update_previous_goodbye
    except:
        return
    cws = get_current_goodbye_settings(event.chat_id)
    if cws:
        """user_added=False,
        user_joined=False,
        user_left=True,
        user_kicked=True"""
        if (event.user_left
                or event.user_kicked) and not (await event.get_user()).bot:
            if CLEAN_WELCOME:
                try:
                    await event.client.delete_messages(event.chat_id,
                                                       cws.previous_goodbye)
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
            current_saved_goodbye_message = None
            if cws and cws.f_mesg_id:
                msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                        ids=int(cws.f_mesg_id))
                file_media = msg_o.media
                current_saved_goodbye_message = msg_o.message
            elif cws and cws.reply:
                current_saved_goodbye_message = cws.reply
            current_message = await event.reply(
                current_saved_goodbye_message.format(mention=mention,
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
            update_previous_goodbye(event.chat_id, current_message.id)


@register(outgoing=True, pattern=r"^.setgoodbye(?: |$)(.*)")
async def save_goodbye(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import add_goodbye_setting
    except:
        await event.edit("`SQL dışı modda çalışıyor!`")
        return
    msg = await event.get_reply_message()
    string = event.pattern_match.group(1)
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#GORUSURUZ_NOTU\
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
    success = "`Görüşürüz mesajı bu sohbet için {} `"
    if add_goodbye_setting(event.chat_id, 0, string, msg_id) is True:
        await event.edit(success.format('kaydedildi'))
    else:
        await event.edit(success.format('güncellendi'))


@register(outgoing=True, pattern="^.checkgoodbye$")
async def show_goodbye(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import get_current_goodbye_settings
    except:
        await event.edit("`SQL dışı modda çalışıyor!`")
        return
    cws = get_current_goodbye_settings(event.chat_id)
    if not cws:
        await event.edit("`Burada kayıtlı karşılama mesajı yok.`")
        return
    elif cws and cws.f_mesg_id:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(cws.f_mesg_id))
        await event.edit(
            "`Şu anda bu not ile çıkanları/ban yiyenlere yanıtlıyorum.`")
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws and cws.reply:
        await event.edit(
            "`Şu anda bu not ile çıkanları/ban yiyenlere yanıtlıyorum.`")
        await event.reply(cws.reply)


@register(outgoing=True, pattern="^.rmgoodbye$")
async def del_goodbye(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import rm_goodbye_setting
    except:
        await event.edit("`SQL dışı modda çalışıyor!`")
        return
    if rm_goodbye_setting(event.chat_id) is True:
        await event.edit("`Karşılama mesajı bu sohbet için silindi.`")
    else:
        await event.edit("`Burada karşılama notu var mı ?`")

CmdHelp('goodbye').add_command(
    'setgoodbye', '<yanıt mesajı> veya .setgoodbye ile bir mesaja cevap verin', 'Mesajı sohbete görüşürüz notu olarak kaydeder.'
).add_command(
    'checkgoodbye', None, 'Sohbette görüşürz notu olup olmadığını kontrol edin.'
).add_command(
    'rmgoodbye', None, 'Geçerli sohbet için görüşürüz notunu siler.'
).add()