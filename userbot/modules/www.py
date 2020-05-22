# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Internet ile alakalı bilgileri edinmek için kullanılan UserBot modülüdür. """

from datetime import datetime

from speedtest import Speedtest
from telethon import functions
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.speed$")
async def speedtst(spd):
    """ .speed komutu sunucu hızını tespit etmek için SpeedTest kullanır. """
    await spd.edit("`Hız testi yapılıyor ...`")
    test = Speedtest()

    test.get_best_server()
    test.download()
    test.upload()
    result = test.results.dict()

    await spd.edit("`"
                   "Başlama Tarihi: "
                   f"{result['timestamp']} \n\n"
                   "İndirme Hızı: "
                   f"{speed_convert(result['download'])} \n"
                   "Yükleme Hızı: "
                   f"{speed_convert(result['upload'])} \n"
                   "Ping: "
                   f"{result['ping']} \n"
                   "İnternet Servis Sağlayıcısı: "
                   f"{result['client']['isp']}"
                   "`")


def speed_convert(size):
    """
    Merhaba Seden, baytları okuyamıyor musun?
    """
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern="^.dc$")
async def neardc(event):
    """ .dc komutu en yakın datacenter bilgisini verir. """
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(f"Şehir : `{result.country}`\n"
                     f"En yakın datacenter : `{result.nearest_dc}`\n"
                     f"Şu anki datacenter : `{result.this_dc}`")


@register(outgoing=True, pattern="^.ping$")
async def pingme(pong):
    """ .ping komutu userbotun ping değerini herhangi bir sohbette gösterebilir.  """
    start = datetime.now()
    await pong.edit("`Pong!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit("`Pong!\n%sms`" % (duration))


CMD_HELP.update(
    {"speed": ".speed\
    \nKullanım: Bir speedtest uygular ve sonucu gösterir."})
CMD_HELP.update(
    {"dc": ".dc\
    \nKullanım: Sunucunuza en yakın datacenter'ı gösterir."})
CMD_HELP.update(
    {"ping": ".ping\
    \nKullanım: Botun ping değerini gösterir."})
