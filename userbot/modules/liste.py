# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the Yusuf Usta Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

from userbot import CMD_HELP
from userbot.events import register
from PIL import Image
import io
import os
import asyncio

@register(outgoing=True, pattern="^.liste ?(gmute|gban)?")
async def liste(event):
    liste = event.pattern_match.group(1)
    try:
        if len(liste) < 1:
            await event.edit("**Bilinmeyen komut!** `Kullanım: .liste gmute/gban`")
            return
    except:
        await event.edit("**Bilinmeyen komut!** `Kullanım: .liste gmute/gban`")
        return
    
    if liste == "gban":
        try:
            from userbot.modules.sql_helper.gban_sql import gbanlist
        except:
            await event.edit("`Sql dışı mod'ta bu özellik çalışmaz!`")
            return
        await event.edit("`Küresel olarak yasaklanan kullanıcılar getiriliyor...`")
        mesaj = ""
        for user in gbanlist():
            mesaj += f"**ID: **`{user.sender}`"

        if len(mesaj) > 4000:
            await event.edit("`Wow! Baya bir kişi yasaklamışsınız. Dosya olarak gönderiyorum...`")
            open("gban_liste.txt", "w+").write(mesaj)
            await event.client.send_message(event.chat_id, f"**Küresel olarak yasakladığınız kullanıcılar**\n\n**İpucu:** Yasakladığınız kullanıcılar hakkında daha fazla bilgi almak için `.whois id` kullanabilirsiniz.", file="gban_liste.txt")
            os.remove("gban_liste.txt")
        else:
            await event.edit(f"**Küresel olarak yasakladığınız kullanıcılar:**\n{mesaj}\n\n**İpucu:** Yasakladığınız kullanıcılar hakkında daha fazla bilgi almak için `.whois id` kullanabilirsiniz.")
    elif liste == "gmute":
        try:
            from userbot.modules.sql_helper.gmute_sql import gmutelist
        except:
            await event.edit("`Sql dışı mod'ta bu özellik çalışmaz!`")
            return
        await event.edit("`Küresel olarak susturulan kullanıcılar getiriliyor...`")
        mesaj = ""
        for user in gmutelist():
            mesaj += f"**ID: **`{user.sender}`"

        if len(mesaj) > 4000:
            await event.edit("`Wow! Baya bir kişi susturmuşsunuz. Dosya olarak gönderiyorum...`")
            open("gmute_liste.txt", "w+").write(mesaj)
            await event.client.send_message(event.chat_id, f"**Küresel olarak susturduğunuz kullanıcılar**\n\n**İpucu:** Susturduğunuz kullanıcılar hakkında daha fazla bilgi almak için `.whois id` kullanabilirsiniz.", file="gmute_liste.txt")
            os.remove("gmute_liste.txt")
        else:
            await event.edit(f"**Küresel olarak susturduğunuz kullanıcılar:**\n{mesaj}\n\n**İpucu:** Susturduğunuz kullanıcılar hakkında daha fazla bilgi almak için `.whois id` kullanabilirsiniz.")

CMD_HELP["liste"] = ".liste gban/gmute\nGbanladığınız ya da Gmutelediğiniz kişileri getirir."