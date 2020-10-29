# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

from userbot.events import register
from eksipy import Baslik, Giri, Eksi
from datetime import datetime
import urllib.parse
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.başlık(\d*) ?(.*)")
async def baslik(event):
    sayfa = event.pattern_match.group(1)
    if sayfa == '':
        sayfa = 1
    else:
        sayfa = int(sayfa)

    baslik = event.pattern_match.group(2)
    try:
        baslik = Baslik(baslik, sayfa)
    except:
        return await event.edit('`Böyle bir başlık bulunamadı.`')
    
    topic = baslik.get_topic()
    entrys = baslik.get_entrys()
    Result = f'**Başlık: **`{topic.title}`\n`{topic.current_page}/{topic.max_page}`\n\n'
    
    for entry in entrys:
        if len(entry.text().strip()) < 450:
            Result += f'`{entry.text().strip()}`\n__[{datetime.utcfromtimestamp(entry.date).strftime("%d/%m/%Y")}](https://eksisozluk.com/entry/{entry.id}) [{entry.author}](https://eksisozluk.com/biri/{urllib.parse.quote(entry.author)})__\n\n'
        else:
            Result += f'**Bu entry uzun gözüküyor.** `.entry {entry.id}` ile alabilirsiniz.\n\n'
    return await event.edit(Result)

@register(outgoing=True, pattern="^.entry ?(\d*)")
async def entry(event):
    Entry = int(event.pattern_match.group(1))
    try:
        Entry = Giri(Entry).get_entry()
    except:
        return await event.edit('`Böyle bir entry bulunamadı.`')
    
    Result = f'**Başlık: **`{Entry.topic.title}`\n\n'
    Result += f'`{Entry.text().strip()}`\n __[{datetime.utcfromtimestamp(Entry.date).strftime("%d/%m/%Y")}](https://eksisozluk.com/entry/{Entry.id}) [{Entry.author}](https://eksisozluk.com/biri/{urllib.parse.quote(Entry.author)})__\n\n'
    return await event.edit(Result)

@register(outgoing=True, pattern="^.g[üu]ndem ?(\d*)$")
async def gundem(event):
    if event.pattern_match.group(1) == '':
        Sayfa = 1
    else:
        Sayfa = int(event.pattern_match.group(1))

    try:
        Gundem = Eksi().gundem(Sayfa)
    except:
        return await event.edit('`Bir hata oluştu.`')
    
    Result = ""
    i = 1
    for Baslik in Gundem:
        Result += f'`{i}-)` [{Baslik.title}]({Baslik.url()}) __{Baslik.giri}__\n'
    return await event.edit(Result)

CmdHelp('eksi').add_command(
    'baslik', '<sayfa> <başlık>', 'Ekşi Sözlükte başlık getirir.', 'baslik2 php'
).add_command(
    'entry', '<id>', 'Entry getirir.', 'entry 1'
).add_command(
    'gundem', '<sayfa>', 'Gündem getirir.', 'gündem 1'
).add()