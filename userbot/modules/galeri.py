# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Coded By Yusuf Usta
# Please give credit.
# Asena UserBot - Yusuf Usta


import io
import re
import asyncio

from userbot import CMD_HELP, ASYNC_POOL, GALERI_SURE
from userbot.events import register
from userbot.main import FotoDegistir

URL_REGEX = re.compile(
    # https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@register(outgoing=True, pattern="^.galeri ?(.*)")
async def degistir(event):
    try:
        import userbot.modules.sql_helper.galeri_sql as sql
    except:
        event.edit("`SQL dışı mod'ta galeri çalışmaz!`")
    secenek = event.pattern_match.group(1)
    secen = secenek.split(" ")
    if secen[0] == "ekle":
        if len(secen) > 1:
            URL = re.search(URL_REGEX, secen[1])
            print(URL)
            if URL != None:
                sql.ekle_foto(secen[1])
                sql.getir_foto()
                await event.edit("`Fotoğraf sıraya alındı.`")
            else:
                await event.edit("`Geçersiz bir resim URL'si girdiniz. Kullanım hakkında bir fikriniz yoksa, ` `.asena galeri` `yazınız.`")
        else:
            await event.edit("`Lütfen bir resim adresi giriniz. Örnek olarak: ` `.galeri ekle https://i.resimyukle.xyz/7Qbbc9.jpeg`")
    elif secen[0] == "liste":
        yfoto = ""
        sql.getir_foto()
        fotolar = sql.TUM_GALERI
        for foto in fotolar:
            yfoto += f"\n▶️ ({foto.g_id}) [Fotoğraf]({foto.foto})"
        await event.edit("**Sıraya Aldığınız Fotoğraflar**\n" + yfoto)
    elif secen[0] == "sil":
        if secen[1].isdigit():
            silme = sql.sil_foto(secen[1])
            if silme == True:
                await event.edit("**Sıradaki fotoğraf başarıyla kaldırıldı**")
            else:
                await event.edit(f"**Sıradaki fotoğraf kaldırılamadı** Hata: {silme}")
        else:
            await event.edit("**Lütfen resmin sırasını belirtiniz. Örnek:** `.galeri sil 2`")
    elif secen[0] == "başla":
        if "galeri" in ASYNC_POOL:
            await event.edit("`Hali hazırda galeri çalışıyor.`")
            return
        ASYNC_POOL.append("galeri")
        sql.getir_foto()
        await event.edit("`Galeri çalışmaya başladı.`")

        while "galeri" in ASYNC_POOL:
            fotolar = sql.TUM_GALERI
            i = 0
            while i < len(fotolar):
                if not "galeri" in ASYNC_POOL:
                    break
                if i == len(fotolar):
                    i = 0
                await FotoDegistir(i)
                await asyncio.sleep(GALERI_SURE)
                i += 1

    elif secen[0] == "kapa":
        if "galeri" in ASYNC_POOL:
            ASYNC_POOL.remove("galeri")
            await event.edit("`Galeri durduruldu!`")
        else:
            event.edit("`Galeri zaten çalışmıyor.`")
        return
    else:
        await event.edit("**Bilinmeyen komut** Kullanım:\nGaleri'ye fotoğraf ekleme: `.galeri ekle https://i.resimyukle.xyz/7Qbbc9.jpeg`\nGaleri listesini görme: `.galeri liste`\nSıradan bir fotoğrafı silme: `.galeri sil <sıra sayısı>`")

CMD_HELP["galeri"] = "Kullanım: Galeri'ye fotoğraf ekleme: `.galeri ekle https://i.resimyukle.xyz/7Qbbc9.jpeg`\nGaleri listesini görme: `.galeri liste`\nSıradan bir fotoğrafı silme: `.galeri sil <sıra sayısı>`"