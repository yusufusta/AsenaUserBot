import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register
import os
import subprocess
import glob

@register(outgoing=True, pattern="^.netease(?: |$)(.*)")
async def netease(event):
    if event.fwd_from:
        return
    song = event.pattern_match.group(1)
    chat = "@WooMaiBot"
    link = f"/netease {song}"
    await event.edit("```Müzik getiriliyor... Lütfen bekleyiniz.```")
    async with bot.conversation(chat) as conv:
          await asyncio.sleep(2)
          await event.edit("`İndiriliyor...Lütfen bekleyiniz.`")
          try:
              msg = await conv.send_message(link)
              response = await conv.get_response()
              respond = await conv.get_response()
              """ - don't spam notif - """
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError:
              await event.reply("```Lütfen @WooMaiBot'un engelini kaldırın ve tekrar deneyin.```")
              return
          await event.edit("`Şarkı gönderiliyor...`")
          await asyncio.sleep(3)
          await bot.send_file(event.chat_id, respond)
    await event.client.delete_messages(conv.chat_id,
                                       [msg.id, response.id, respond.id])
    await event.delete()

@register(outgoing=True, pattern="^.deez(?: |$)(.*)")
async def sddd(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit("`Bana Spotify ya da Deezer linki ver.`**(._.)**")
    else:
        await event.edit("**Initiating Download!**")
    chat = "@DeezLoadBot"
    async with bot.conversation(chat) as conv:
          try:
              msg_start = await conv.send_message("/start")
              response = await conv.get_response()
              r = await conv.get_response()
              msg = await conv.send_message(d_link)
              details = await conv.get_response()
              song = await conv.get_response()
              """ - don't spam notif - """
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError:
              await event.edit("**Hata:** @DeezLoadBot`'un engelini kaldır ve tekrar dene`")
              return
          await bot.send_file(event.chat_id, song, caption=details.text)
          await event.client.delete_messages(conv.chat_id,
                                             [msg_start.id, response.id, r.id, msg.id, details.id, song.id])
          await event.delete()

@register(outgoing=True, pattern="^.spot(?: |$)(.*)")
async def smdd(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@SpotifyMusicDownloaderBot"
    await event.edit("```Müzik getiriliyor...```")
    async with bot.conversation(chat) as conv:
          await asyncio.sleep(2)
          await event.edit("`İndirme işlemi biraz zaman alabilir, lütfen bekleyiniz.`")
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=752979930))
              msg = await bot.send_message(chat, link)
              respond = await response
              res = conv.wait_event(events.NewMessage(incoming=True,from_users=752979930))
              r = await res
              """ - don't spam notif - """
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError:
              await event.reply("```@SpotifyMusicDownloaderBot engelini aç ve tekrar dene.```")
              return
          await bot.forward_messages(event.chat_id, respond.message)
    await event.client.delete_messages(conv.chat_id,
                                       [msg.id, r.id, respond.id])
    await event.delete()

@register(outgoing=True, pattern="^.song(?: |$)(.*)")
async def port_song(event):
    if event.fwd_from:
        return
    
    cmd = event.pattern_match.group(1)
    if len(cmd) < 1:
        await event.edit("`Kullanım: .song şarkı ismi/youtube url/spotify url`") 

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
        
    await event.edit("`Şarkı aranıyor ve indiriliyor lütfen bekleyin!`")  
    dosya = os.getcwd() 
    os.system(f"spotdl --song {cmd} -f {dosya}")
    await event.edit("`İndirme işlemi başarılı lütfen bekleyiniz.`")    

    l = glob.glob("*.mp3")
    if len(i) >= 1:
        await event.edit("Şarkı yükleniyor!")
        await event.client.send_file(
            event.chat_id,
            l[0],
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id
        )
        await event.delete()
    else:
        await event.edit("`Aradığınız şarkı bulunamadı! Üzgünüm.`")   
        return 
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3",shell=True)

@register(outgoing=True, pattern="^.songpl ?(.*)")
async def songpl(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)

    if len(cmd) < 1:
        await event.edit("Kullanım: .songpl spotify playlist url")    

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.edit("`Playlist aranıyor ve indiriliyor lütfen bekleyin!`")
    dosya = os.getcwd() + "/playlist/" + "pl.pl"
    klasor = os.getcwd() + "/playlist/"
    sonuc = os.system(f"spotdl --playlist {cmd} --write-to=\"{dosya}\"")
    sonuc2 = os.system(f"spotdl --list {dosya} -f {klasor}")
    await event.edit("`İndirme başarılı! Şimdi yükleniyor.`")
    l = glob.glob(f"{klasor}/*.mp3")
    i = 0
    if len(l) >= 1:
        while i < len(l):
            await event.reply("Şarkı gönderiliyor! Şarkı: " + l[i])
            await event.client.send_file(
                event.chat_id,
                l[i],
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
    else:
        await event.edit("`Aradığınız playlist bulunamadı! Üzgünüm.`")   
        return 
    os.system(f"rm -rf {klasor}/*.mp3")
    subprocess.check_output(f"rm -rf {klasor}/*.mp3",shell=True)
    os.system(f"rm -rf {klasor}/*.pl")
    subprocess.check_output(f"rm -rf {klasor}/*.pl",shell=True)

CMD_HELP.update({'song': 
    "`.netease Şarkı`"
    "\nKullanım: @WooMaiBot Bot'undan şarkı indirir"
    "\n\n`.sdd <Spotify/Deezer Link>`"
    "\nKullanım: Spotify ya da Deezer şarkı indirir"
    "\n\n`.smd Şarkı`"
    "\nKullanım: Spotify'dan şarkı indirir"
    "\n\n`.song Youtube/Spotify/Şarkı`"
    "\nKullanım: Şarkı indirir"
    "\n\n`.songpl Spotify Playlist`"
    "\nKullanım: Spotify Playlist'inden şarkı indirir"


})
