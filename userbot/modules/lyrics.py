# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


import os
import lyricsgenius
import random
import asyncio

from userbot.events import register
from userbot import CMD_HELP, LOGS, GENIUS

@register(outgoing=True, pattern="^.lyrics(?: |$)(.*)")
async def lyrics(lyric):
    if r"-" in lyric.text:
        pass
    else:
        await lyric.edit("`Hata: lütfen <sanatçı> ve <şarkı> için bölücü olarak '-' kullanın`\n"
                         "Örnek: `Stabil - Reenkarne`")
        return

    if GENIUS is None:
        await lyric.edit(
            "`Lütfen Genius tokeni ayarlayınız. Teşekkürler!`")
        return
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = lyric.text.split('.lyrics')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except:
            await lyric.edit("`Lütfen sanatçı ve şarkı ismini veriniz`")
            return

    if len(args) < 1:
        await lyric.edit("`Lütfen sanatçı ve şarkı ismini veriniz`")
        return

    await lyric.edit(f"`{artist} - {song} için şarkı sözleri aranıyor...`")

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lyric.edit(f"Şarkı **{artist} - {song}** bulunamadı!")
        return
    if len(songs.lyrics) > 4096:
        await lyric.edit("`Şarkı sözleri çok uzun, görmek için dosyayı görüntüleyin.`")
        with open("lyrics.txt", "w+") as f:
            f.write(f"Arama sorgusu: \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
        )
        os.remove("lyrics.txt")
    else:
        await lyric.edit(f"**Arama sorgusu**: \n`{artist} - {song}`\n\n```{songs.lyrics}```")
    return

@register(outgoing=True, pattern="^.singer(?: |$)(.*)")
async def singer(lyric):
    if r"-" in lyric.text:
        pass
    else:
        await lyric.edit("`Hata: lütfen <sanatçı> ve <şarkı> için bölücü olarak '-' kullanın`\n"
                         "Örnek: `Duman - Haberin Yok Ölüyorum`")
        return

    if GENIUS is None:
        await lyric.edit(
            "`Lütfen Genius tokeni ayarlayınız. Teşekkürler!`")
        return
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = lyric.text.split('.singer')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except:
            await lyric.edit("`Lütfen sanatçı ve şarkı ismini veriniz`")
            return

    if len(args) < 1:
        await lyric.edit("`Lütfen sanatçı ve şarkı ismini veriniz`")
        return

    await lyric.edit(f"`{artist} - {song} için şarkı sözleri aranıyor...`")

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lyric.edit(f"Şarkı **{artist} - {song}** bulunamadı!")
        return
    await lyric.edit(f"🎙 Kulaklarınız pasını sileceğim! {artist}'dan {song} geliyor!")
    await asyncio.sleep(1)

    split = songs.lyrics.splitlines()
    i = 0
    while i < len(split):
        try:
            if split[i] != None:
                await lyric.edit(split[i])
                await asyncio.sleep(2)
            i += 1
        except:
            i += 1
    await lyric.edit(f"🎙Çok güzel söyledim, değil mi?")

    return

            

CMD_HELP.update({
    "lyrics":
    "Kullanım: .`lyrics <sanatçı adı> - <şarkı ismi>`\n"
    "NOT: ""-"" ayracı önemli!",
    "singer":
    "Şarkı söyler, Kullanım: .`singer <sanatçı adı> - <şarkı ismi>`\n"
    "NOT: ""-"" ayracı önemli!"

})
