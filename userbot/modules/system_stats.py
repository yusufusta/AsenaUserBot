# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Sunucu hakkında bilgi veren UserBot modülüdür. """

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which
from os import remove
from telethon import version
import random
from userbot import CMD_HELP
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
# ================= CONSTANT =================
DEFAULTUSER = uname().node
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
        await sysd.edit("`Öncelikle neofetch modülünü yükleyin !!`")


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

        await event.edit("`UserBot Versiyonu: "
                         f"{verout}"
                         "` \n"
                         "`Toplam değişiklik: "
                         f"{revout}"
                         "`")
    else:
        await event.edit(
            "Bu arada Asena seni çok seviyor. ❤"
        )


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
async def pipcheck(pip):
    """ .pip komutu python-pip araması yapar. """
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit("`Aranıyor . . .`")
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
                await pip.edit("`Çıktı çok büyük, dosya olarak gönderiliyor.`")
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
            await pip.edit("**Sorgu: **\n`"
                           f"{invokepip}"
                           "`\n**Sonuç: **\n`"
                           f"{pipout}"
                           "`")
        else:
            await pip.edit("**Sorgu: **\n`"
                           f"{invokepip}"
                           "`\n**Sonuç: **\n`Bir şey bulunamadı.`")
    else:
        await pip.edit("`Bir örnek görmek için .asena pip komutunu kullanın.`")


@register(outgoing=True, pattern="^.alive$")
async def amialive(e):
    await e.edit(f"{PLUGIN_MESAJLAR['alive']}")


CMD_HELP.update(
    {"sysd": ".sysd\
    \nKullanım: Neofetch modülünü kullanarak sistem bilgisi gösterir."})
CMD_HELP.update({"botver": ".botver\
    \nKullanım: Userbot sürümünü gösterir."})
CMD_HELP.update(
    {"pip": ".pip <module(s)>\
    \nKullanım: Pip modüllerinde arama yapar."})
CMD_HELP.update({
    "alive": ".alive\
    \nKullanım: Asena botunun çalışıp çalışmadığını kontrol etmek için kullanılır."
})
