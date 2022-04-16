# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

""" Olayları yönetmek için UserBot modülü.
 UserBot'un ana bileşenlerinden biri. """

import sys
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from os import remove
from time import gmtime, strftime
from traceback import format_exc

from telethon import events

from userbot import bot, BOTLOG_CHATID, LOGSPAMMER, PATTERNS


def register(**args):
    """ Yeni bir etkinlik kaydedin. """
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    groups_only = args.get('groups_only', False)
    trigger_on_fwd = args.get('trigger_on_fwd', False)
    trigger_on_inline = args.get('trigger_on_inline', False)
    disable_errors = args.get('disable_errors', False)

    if pattern:
        args["pattern"] = pattern.replace("^.", "^["+ PATTERNS + "]")
    if "disable_edited" in args:
        del args['disable_edited']

    if "ignore_unsafe" in args:
        del args['ignore_unsafe']

    if "groups_only" in args:
        del args['groups_only']

    if "disable_errors" in args:
        del args['disable_errors']

    if "trigger_on_fwd" in args:
        del args['trigger_on_fwd']
      
    if "trigger_on_inline" in args:
        del args['trigger_on_inline']

    def decorator(func):
        async def wrapper(check):
            if not LOGSPAMMER:
                send_to = check.chat_id
            else:
                send_to = BOTLOG_CHATID

            if not trigger_on_fwd and check.fwd_from:
                return

            if check.via_bot_id and not trigger_on_inline:
                return
             
            if groups_only and not check.is_group:
                await check.respond("`Bunun bir grup olduğunu sanmıyorum.`")
                return

            try:
                await func(check)
                

            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException:
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**USERBOT HATA RAPORU**\n"
                    link = "[Asena Destek Grubu](https://t.me/AsenaSupport)"
                    text += "İsterseniz, bunu rapor edebilirsiniz"
                    text += f"- sadece bu mesajı buraya iletin {link}.\n"
                    text += "Hata ve Tarih dışında hiçbir şey kaydedilmez\n"

                    ftext = "========== UYARI =========="
                    ftext += "\nBu dosya sadece burada yüklendi,"
                    ftext += "\nsadece hata ve tarih kısmını kaydettik,"
                    ftext += "\ngizliliğinize saygı duyuyoruz,"
                    ftext += "\nburada herhangi bir gizli veri varsa"
                    ftext += "\nbu hata raporu olmayabilir, kimse verilerinize ulaşamaz.\n"
                    ftext += "================================\n\n"
                    ftext += "--------USERBOT HATA GUNLUGU--------\n"
                    ftext += "\nTarih: " + date
                    ftext += "\nGrup ID: " + str(check.chat_id)
                    ftext += "\nGönderen kişinin ID: " + str(check.sender_id)
                    ftext += "\n\nOlay Tetikleyici:\n"
                    ftext += str(check.text)
                    ftext += "\n\nGeri izleme bilgisi:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nHata metni:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------USERBOT HATA GUNLUGU BITIS--------"

                    command = "git log --pretty=format:\"%an: %s\" -10"
                    ftext += "\n\n\nUserbot ID: QXNlbmEgVGVsZWdyYW0*"
                    ftext += "\nSon 10 commit:\n"

                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("error.log", "w+")
                    file.write(ftext)
                    file.close()

                    if LOGSPAMMER:
                        await check.client.respond("`Üzgünüm, UserBot'um çöktü.\
                        \nHata günlükleri UserBot günlük grubunda saklanır.`")

                    await check.client.send_file(send_to,
                                                 "error.log",
                                                 caption=text)
                    remove("error.log")
            else:
                pass
        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))

        return wrapper

    return decorator
