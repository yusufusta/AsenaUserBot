# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the Yusuf Usta Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

import re
import userbot.modules.sql_helper.mesaj_sql as sql
from userbot import CMD_HELP
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR, ORJ_PLUGIN_MESAJLAR

@register(outgoing=True, pattern="^.değiştir ?(.*)")
async def degistir(event):
    plugin = event.pattern_match.group(1)
    mesaj = re.search(r"\"(.*)\"", plugin)

    if mesaj:
        rege = re.findall(r"(?:|$)(.*)\"(.*)\"", plugin)
        plugin = rege[0][0]
        mesaj = rege[0][1]
    else:
        mesaj = []

    plugin = plugin.strip()
    TURLER = ["afk", "alive", "pm", "kickme", "dızcı", "ban", "mute", "approve", "disapprove"]
    if type(mesaj) == list:
        if plugin in TURLER:
            silme = sql.sil_mesaj(plugin)
            if silme == True:
                PLUGIN_MESAJLAR[plugin] = ORJ_PLUGIN_MESAJLAR[plugin]
                await event.edit("`Plugin mesajı başarıyla silindi.`")
            else:
                await event.edit(f"**Plugin mesajı silinemedi.** Hata: `{silme}`")
        else:
            await event.edit("**Bilinmeyen plugin.** Mesajını silebileceğiniz pluginler: `afk/alive/pm/kickme/dızcı/ban/mute/approve/disapprove`")
    elif len(plugin) < 1:
        await event.edit("**Değiştir, bottaki plugin-mesajlarını değiştirmenize yarar.**\nÖrnek Kullanım: `.değiştir afk \"Şu an burda değilim... Belki hiç gelmem\"`\nPlugin-mesajı silme: `.değiştir afk`\nDeğiştirebileceğiniz plugin-mesajları (şu anlık): `afk/alive/pm/kickme/dızcı/ban/mute/approve/disapprove`")
    elif type(mesaj) == str:
        if plugin in TURLER:
            if mesaj.isspace():
                await event.edit(f"**Plugin mesajı boş olamaz.**")
                return
            else:
                PLUGIN_MESAJLAR[plugin] = mesaj
                sql.ekle_mesaj(plugin, mesaj)
                await event.edit(f"Plugin(`{plugin}`) için mesajınız(`{mesaj}`) ayarlandı.")
        else:
            await event.edit("**Bilinmeyen plugin.** Değiştirebileceğiniz pluginler: `afk/alive/pm/kickme/dızcı/ban/mute/approve/disapprove`")

CMD_HELP.update({'degistir': '.değiştir <modül> <mesaj>\
        \nKullanım: **Değiştir, bottaki plugin-mesajlarını değiştirmenize yarar.**\nÖrnek Kullanım: `.değiştir afk \"Şu an burda değilim... Belki hiç gelmem\"`\nPlugin-mesajı silme: `.değiştir afk`\nDeğiştirebileceğiniz plugin-mesajları (şu anlık): `afk/alive/pm/kickme/dızcı/ban/mute/approve/disapprove`'})
