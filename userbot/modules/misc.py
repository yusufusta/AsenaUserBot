# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Birkaç küçük komutu içeren UserBot modülü. """

from random import randint
from asyncio import sleep
from os import execl
import sys
import os
import io
import sys
import json
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern="^.resend")
async def resend(event):
    await event.delete()
    m = await event.get_reply_message()
    if not m:
        event.edit("`Bir dosyaya yanıt ver.`")
        return
    await event.respond(m)

@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ .random komutu, eşya listesinden rastgele bir eşya seçer. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            "`2 veya daha fazla eşya gerekli. Daha fazla bilgi için .seden random komutunu gir.`"
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit("**Sorgu: **\n`" + items.text[8:] + "`\n**Çıktı: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
async def sleepybot(time):
    """ .sleep komutu Seden'in birkaç saniye uyumasına olanak sağlar. """
    if " " not in time.pattern_match.group(1):
        await time.reply("Kullanım Şekli: `.sleep [saniye]`")
    else:
        counter = int(time.pattern_match.group(1))
        await time.edit("`Horlayarak uyuyorum...`")
        await sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                "Botu" + str(counter) + "saniye uykuya bıraktın.",
            )
        await sleep(counter)
        await time.edit("`Günaydın!`")


@register(outgoing=True, pattern="^.shutdown$")
async def shutdown(event):
    """ .shutdown komutu botu kapatır. """
    await event.edit("`Görüşürüz... *Windows XP kapanma sesi*`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot kapatıldı.")
    try:
        await bot.disconnect()
    except:
        pass


@register(outgoing=True, pattern="^.restart$")
async def restart(event):
    await event.edit("`Bot yeniden başlatılıyor...`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "Bot yeniden başlatıldı.")

    try:
        await bot.disconnect()
    except:
        pass

    execl(sys.executable, sys.executable, *sys.argv)


@register(outgoing=True, pattern="^.support$")
async def bot_support(wannahelp):
    """ .support komutu destek grubumuzu verir. """
    await wannahelp.edit("[Buradan](http://t.me/AsenaSupport) destek grubumuza ulaşabilirsiniz.")


@register(outgoing=True, pattern="^.creator$")
async def creator(e):
    await e.edit("Bu bot \n"
                 "[Yusuf Usta](https://t.me/Qulec) tarafından geliştirilmiştir. \n")


@register(outgoing=True, pattern="^.readme$")
async def reedme(e):
    await e.edit("[Asena README.md](https://github.com/quiec/AsenaUserBot/blob/seden/README.md)")


# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(' ', 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ .repo komutunun tek yaptığı şey GitHub repomuzun bağlantısını vermek. """
    await wannasee.edit("[Asena Repo](https://github.com/quiec/asenauserbot)")


@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit(
            "`Çözülmüş mesaj için userbot loglarını kontrol et!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Çözülen mesaj`")


CMD_HELP.update({
    'random':
    '.random <eşya1> <eşya2> ... <eşyaN>\
\nKullanım: Eşya listesinden rastgele bir eşya seçer'
})

CMD_HELP.update({
    'sleep':
    '.sleep <saniye>\
\nKullanım: Seden de bir insan, o da yoruluyor. Ara sıra biraz uyumasına izin ver.'
})

CMD_HELP.update({
    "shutdown":
    ".shutdown\
\nKullanım: Bazen canın botunu kapatmak ister. Gerçekten o nostaljik\
Windows XP kapanış sesini duyabileceğini zannedersin..."
})

CMD_HELP.update(
    {'support': ".support\
\nKullanım: Yardıma ihtiyacın olursa bu komutu kullan."
     })

CMD_HELP.update({
    'repo':
    '.repo\
\nKullanım: Seden UserBot GitHub reposu'
})

CMD_HELP.update({
    "readme":
    ".readme\
\nKullanım: Asena botunun GitHub'daki README.md dosyasına giden bir bağlantı."
})

CMD_HELP.update(
    {"creator": ".creator\
\nKullanım: Bu güzel botu kimlerin oluşturduğunu öğren :-)"})

CMD_HELP.update({
    "repeat":
    ".repeat <sayı> <metin>\
\nKullanım: Bir metni belli bir sayıda tekrar eder. Spam komutu ile karıştırma!"
})

CMD_HELP.update({"restart": ".restart\
\nKullanım: Botu yeniden başlatır."})

CMD_HELP.update({"resend": ".resend\
\nKullanım: Bir medyayı yeniden gönderir."})

CMD_HELP.update({
    "raw":
    ".raw\
\nKullanım: Kullanılan mesaj hakkında JSON'a benzer bir şekilde detaylı bilgiler verir."
})
