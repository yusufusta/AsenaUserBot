# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Sunucu hakkında bilgi veren UserBot modülüdür. """

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import uname
from shutil import which
from os import remove
from userbot import CMD_HELP, ASENA_VERSION
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from telethon import version
from platform import python_version
from userbot.cmdhelp import CmdHelp

# ================= CONSTANT =================
DEFAULTUSER = uname().node
# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("system_stats")

# ████████████████████████████████ #
# ============================================

@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
    """ .sysd komutu neofetch kullanarak sistem bilgisini gösterir. """
    try:
        neo = "neofetch --stdout"
        fetch = await asyncrunapp(
            neo,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await fetch.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await sysd.edit("`" + result + "`")
    except FileNotFoundError:
        await sysd.edit(LANG['NO_NEOFETCH'])


@register(outgoing=True, pattern="^.botver$")
async def bot_ver(event):
    """ .botver komutu bot versiyonunu gösterir. """
    if which("git") is not None:
        invokever = "git describe --all --long"
        ver = await asyncrunapp(
            invokever,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        invokerev = "git rev-list --all --count"
        rev = await asyncrunapp(
            invokerev,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await event.edit(f"`{LANG['VERSION']}: "
                         f"{verout}"
                         "` \n"
                         f"`{LANG['REVOUT']}: "
                         f"{revout}"
                         "`")
    else:
        await event.edit(
            "Tanrı Türk'ü Korusun 🐺"
        )


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
async def pipcheck(pip):
    """ .pip komutu python-pip araması yapar. """
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit(f"`{LANG['SEARCHING']} . . .`")
        invokepip = f"pip3 search {pipmodule}"
        pipc = await asyncrunapp(
            invokepip,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit(LANG['BIG'])
                file = open("output.txt", "w+")
                file.write(pipout)
                file.close()
                await pip.client.send_file(
                    pip.chat_id,
                    "output.txt",
                    reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit(f"**{LANG['QUERY']}: **\n`"
                           f"{invokepip}"
                           f"`\n**{LANG['RESULT']}: **\n`"
                           f"{pipout}"
                           "`")
        else:
            await pip.edit(f"**{LANG['QUERY']}: **\n`"
                           f"{invokepip}"
                           f"`\n**{LANG['RESULT']}: **\n`{LANG['NOT_FOUND']}.`")
    else:
        await pip.edit(LANG['EXAMPLE'])

@register(outgoing=True, pattern="^.alive$")
async def amialive(e):
    me = await e.client.get_me()
    if type(PLUGIN_MESAJLAR['alive']) == str:
        await e.edit(PLUGIN_MESAJLAR['alive'].format(
            telethon=version.__version__,
            python=python_version(),
            asena=ASENA_VERSION,
            plugin=len(CMD_HELP),
            id=me.id,
            username='@' + me.username if me.username else f'[{me.first_name}](tg://user?id={me.id})',
            first_name=me.first_name,
            last_name=me.last_name if me.last_name else '',
            mention=f'[{me.first_name}](tg://user?id={me.id})'
        ))
    else:
        await e.delete()
        if not PLUGIN_MESAJLAR['alive'].text == '':
            PLUGIN_MESAJLAR['alive'].text = PLUGIN_MESAJLAR['alive'].text.format(
                telethon=version.__version__,
                python=python_version(),
                asena=ASENA_VERSION,
                plugin=len(CMD_HELP),
                id=me.id,
                username='@' + me.username if me.username else f'[{me.first_name}](tg://user?id={me.id})',
                first_name=me.first_name,
                last_name=me.last_name if me.last_name else '',
                mention=f'[{me.first_name}](tg://user?id={me.id})'
            )
        if e.is_reply:
            await e.respond(PLUGIN_MESAJLAR['alive'], reply_to=e.message.reply_to_msg_id)
        else:
            await e.respond(PLUGIN_MESAJLAR['alive'])


CmdHelp('system_stats').add_command(
    'sysd', None, 'Neofetch modülünü kullanarak sistem bilgisi gösterir.'
).add_command(
    'botver', None, 'Userbot sürümünü gösterir.'
).add_command(
    'pip', '<modül(ler)>', 'Pip modüllerinde arama yapar.'
).add_command(
    'alive', None, 'Asena botunun çalışıp çalışmadığını kontrol etmek için kullanılır.'
).add()