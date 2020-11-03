# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta
#

""" AFK ile ilgili komutları içeren UserBot modülü """

from random import randint
from asyncio import sleep

from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN, SON_GORULME)
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from time import time
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("afk")

# ████████████████████████████████ #

def time_formatter(seconds, short=True):
    # Thanks UsergeTeam #
    # https://github.com/UsergeTeam/Userge/blob/053786a1ed54530b305c1bfb96e70147ca99463f/userge/utils/tools.py#L70 #
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + (" gün, " if not short else "g, ")) if days else "") + \
        ((str(hours) + (" saat, " if not short else "s, ")) if hours else "") + \
        ((str(minutes) + (" dakika, " if not short else "d, ")) if minutes else "") + \
        ((str(seconds) + (" saniye, " if not short else "s, ")) if seconds else "")
    return tmp[:-2] + " önce"

@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ Bu fonksiyon biri sizi etiketlediğinde sizin AFK olduğunuzu bildirmeye yarar."""
    global COUNT_MSG
    global USERS
    global ISAFK
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            from_user = await mention.get_sender()
            if from_user.username:
                username = '@' + from_user.username
            else:
                username = f'[{from_user.first_name} {from_user.last_name}](tg://user?id={from_user.id})'
            
            mention_format = f'[{from_user.first_name}](tg://user?id={from_user.id})'
            first_name = from_user.first_name

            if from_user.last_name:
                last_name = from_user.last_name
            else:
                last_name = ''

            last_seen_seconds = round(time() - SON_GORULME)
            last_seen = time_formatter(last_seen_seconds)
            last_seen_long = time_formatter(last_seen_seconds, False)

            if mention.sender_id not in USERS:
                if AFKREASON:
                    if type(PLUGIN_MESAJLAR['afk']) is str:
                        await mention.reply(PLUGIN_MESAJLAR['afk'].format(
                        username=username,
                        mention=mention_format,
                        first_name=first_name,
                        last_name=last_name,
                        last_seen_seconds=last_seen_seconds,
                        last_seen=last_seen,
                        last_seen_long=last_seen_long
                    ) \
                            + f"\n{LANG['REASON']}: `{AFKREASON}`\n")
                    else:
                        msj = await mention.reply(PLUGIN_MESAJLAR['afk'])
                        await msj.reply(f"{LANG['REASON']}: `{AFKREASON}`")
                else:
                    if not isinstance(PLUGIN_MESAJLAR['afk'], str):
                        PLUGIN_MESAJLAR['afk'].text = PLUGIN_MESAJLAR['afk'].text.format(
                            username=username,
                            mention=mention_format,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long
                        )
                        await mention.reply(PLUGIN_MESAJLAR['afk'])
                    else:
                        await mention.reply(PLUGIN_MESAJLAR['afk'].format(
                            username=username,
                            mention=mention_format,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long
                        ))
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        if PLUGIN_MESAJLAR['afk'] is str:
                            await mention.reply(PLUGIN_MESAJLAR['afk'].format(
                            username=username,
                            mention=mention_format,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long
                            ) \
                                + f"\{LANG['REASON']}: `{AFKREASON}`")
                        else:
                            msj = await mention.reply(PLUGIN_MESAJLAR['afk'])
                            await msj.reply(f"{LANG['REASON']}: `{AFKREASON}`")
                    else:
                        if not isinstance(PLUGIN_MESAJLAR['afk'], str):
                            PLUGIN_MESAJLAR['afk'].text = PLUGIN_MESAJLAR['afk'].text.format(
                                username=username,
                                mention=mention_format,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long
                            )
                            await mention.reply(PLUGIN_MESAJLAR['afk'])
                        else:
                            await mention.reply(PLUGIN_MESAJLAR['afk'].format(
                                username=username,
                                mention=mention_format,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long
                            ))

                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Siz afk iken PM atanları afk olduğunuza dair bildirmeye yarayan fonksiyondur. """
    global ISAFK
    global USERS
    global COUNT_MSG
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        
        from_user = await sender.get_sender()
        if from_user.username:
            username = '@' + from_user.username
        else:
            username = f'[{from_user.first_name} {from_user.last_name}](tg://user?id={from_user.id})'
        
        mention = f'[{from_user.first_name}](tg://user?id={from_user.id})'
        first_name = from_user.first_name

        if from_user.last_name:
            last_name = from_user.last_name
        else:
            last_name = ''

        last_seen_seconds = round(time() - SON_GORULME)
        last_seen = time_formatter(last_seen_seconds)
        last_seen_long = time_formatter(last_seen_seconds, False)

        if apprv and ISAFK:
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(LANG['AFK'].format(
                        username=username,
                        mention=mention,
                        first_name=first_name,
                        last_name=last_name,
                        last_seen_seconds=last_seen_seconds,
                        last_seen=last_seen,
                        last_seen_long=last_seen_long
                    ) \
                    + f"\n{LANG['REASON']}: `{AFKREASON}`")
                else:
                    if not isinstance(PLUGIN_MESAJLAR['afk'], str):
                        PLUGIN_MESAJLAR['afk'].text = PLUGIN_MESAJLAR['afk'].text.format(
                            username=username,
                            mention=mention,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long
                        )
                        await sender.reply(PLUGIN_MESAJLAR['afk'])
                    else:
                        await sender.reply(PLUGIN_MESAJLAR['afk'].format(
                            username=username,
                            mention=mention,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long
                        ))

                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        if type(PLUGIN_MESAJLAR['afk']) is str:
                            await sender.reply({PLUGIN_MESAJLAR['afk']}.format(
                                username=username,
                                mention=mention,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long
                            ) \
                            + f"\n{LANG['REASON']}: `{AFKREASON}`")
                        else:
                            msj = await sender.reply(PLUGIN_MESAJLAR['afk'])
                            await msj.reply(f"{LANG['REASON']}: `{AFKREASON}`")
                    else:
                        if not isinstance(PLUGIN_MESAJLAR['afk'], str):
                            PLUGIN_MESAJLAR['afk'].text = PLUGIN_MESAJLAR['afk'].text.format(
                                username=username,
                                mention=mention,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long
                            )

                            await sender.reply(PLUGIN_MESAJLAR['afk'])
                        else:
                            await sender.reply(PLUGIN_MESAJLAR['afk'].format(
                                username=username,
                                mention=mention,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long
                            ))

                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ .afk komutu siz afk iken insanları afk olduğunuza dair bilgilendirmeye yarar. """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    global SON_GORULME

    if string:
        AFKREASON = string
        await afk_e.edit(f"{LANG['IM_AFK']}\
        \n{LANG['REASON']}: `{string}`")
    else:
        await afk_e.edit(LANG['IM_AFK'])

    SON_GORULME = time()
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nAFK oldunuz.")
    ISAFK = True
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ Bu kısım bir yere bir şey yazdığınızda sizi AFK modundan çıkarmaya yarar. """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if ISAFK:
        ISAFK = False
        await notafk.respond(LANG['IM_NOT_AFK'])
        await sleep(2)
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "Siz AFK iken " + str(len(USERS)) + " kişi size " +
                str(COUNT_MSG) + " mesaj gönderdi.",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                    " size " + "`" + str(USERS[i]) + " mesaj gönderdi`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None

CmdHelp('afk').add_command(
    'afk', 
    '<İsteğe bağlı sebep>', 
    'AFK olduğunuzu belirtir. Kim size pm atarsa ya da sizi etiketlerse sizin AFK olduğunuzu ve belirlediğiniz sebebi gösterir. Herhangi bir yere mesaj yazdığınızda AFK modu kapanır.'
    ).add()