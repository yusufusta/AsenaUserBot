# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the  GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

from userbot import CMD_HELP
from userbot.events import register
from PIL import Image
import io
import os
import asyncio
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("cevir")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.çevir ?(foto|ses|gif|mp3)? ?(.*)")
@register(outgoing=True, pattern="^.convt ?(gif|voice|photo|mp3)? ?(.*)")
async def cevir(event):
    islem = event.pattern_match.group(1)
    try:
        if len(islem) < 1:
            await event.edit(LANG['INVALID_COMMAND'])
            return
    except:
        await event.edit(LANG['INVALID_COMMAND'])
        return

    if islem == "foto" or islem == "photo":
        rep_msg = await event.get_reply_message()

        if not event.is_reply or not rep_msg.sticker:
            await event.edit(LANG['NEED_REPLY'])
            return
        await event.edit(LANG['CONVERTING_TO_PHOTO'])
        foto = io.BytesIO()
        foto = await event.client.download_media(rep_msg.sticker, foto)

        im = Image.open(foto).convert("RGB")
        im.save("sticker.png", "png")
        await event.client.send_file(event.chat_id, "sticker.png", reply_to=rep_msg, caption="@AsenaUserBot `ile fotoğrafa çevirildi.`")

        await event.delete()
        os.remove("sticker.png")
    elif islem == "ses" or islem == "voice":
        EFEKTLER = ["çocuk", "robot", "earrape", "hızlı", "parazit", "yankı"]
        # https://www.vacing.com/ffmpeg_audio_filters/index.html #
        KOMUT = {"çocuk": '-filter_complex "rubberband=pitch=1.5"', "robot": '-filter_complex "afftfilt=real=\'hypot(re,im)*sin(0)\':imag=\'hypot(re,im)*cos(0)\':win_size=512:overlap=0.75"', "earrape": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"', "hızlı": "-filter_complex \"rubberband=tempo=1.5\"", "parazit": '-filter_complex "afftfilt=real=\'hypot(re,im)*cos((random(0)*2-1)*2*3.14)\':imag=\'hypot(re,im)*sin((random(1)*2-1)*2*3.14)\':win_size=128:overlap=0.8"', "yankı": "-filter_complex \"aecho=0.8:0.9:500|1000:0.2|0.1\""}
        efekt = event.pattern_match.group(2)

        if len(efekt) < 1:
            await event.edit(LANG['NEED_EFECT'])
            return

        rep_msg = await event.get_reply_message()

        if not event.is_reply or not (rep_msg.voice or rep_msg.audio):
            await event.edit(LANG['NEED_SOUND'])
            return

        await event.edit(LANG['EFECTING'])
        if efekt in EFEKTLER:
            indir = await rep_msg.download_media()
            ses = await asyncio.create_subprocess_shell(f"ffmpeg -i '{indir}' {KOMUT[efekt]} output.mp3")
            await ses.communicate()
            await event.client.send_file(event.chat_id, "output.mp3", reply_to=rep_msg, caption="@AsenaUserBot `ile efekt uygulandı.`")
            
            await event.delete()
            os.remove(indir)
            os.remove("output.mp3")
        else:
            await event.edit(LANG['NOT_FOUND_EFECT'])
    elif islem == "gif":
        rep_msg = await event.get_reply_message()

        if not event.is_reply or (not rep_msg.video) and (not rep_msg.document.mime_type == 'application/x-tgsticker'):
            await event.edit(LANG['NEED_VIDEO'])
            return

        await event.edit(LANG['CONVERTING_TO_GIF'])
        video = io.BytesIO()
        video = await event.client.download_media(rep_msg)
        if rep_msg.document.mime_type == 'application/x-tgsticker':
            print(f"lottie_convert.py '{video}' out.gif")
            gif = await asyncio.create_subprocess_shell(f"lottie_convert.py '{video}' out.gif")
        else:
            gif = await asyncio.create_subprocess_shell(f"ffmpeg -i '{video}' -filter_complex 'fps=20,scale=320:-1:flags=lanczos,split [o1] [o2];[o1] palettegen [p]; [o2] fifo [o3];[o3] [p] paletteuse' out.gif")
        await gif.communicate()
        await event.edit(f"`{LANG['UPLOADING_GIF']}`")

        try:
            await event.client.send_file(event.chat_id, "out.gif",reply_to=rep_msg, caption=LANG['WITH_ASENA_GIF'])
        except:
            await event.edit(LANG['ERROR'])
            await event.delete()
            os.remove("out.gif")
            os.remove(video)
        finally:
            await event.delete()
            os.remove("out.gif")
            os.remove(video)
    elif islem == "mp3":
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not rep_msg.video:
            await event.edit(LANG['NEED_VIDEO'])
            return
        await event.edit('`Sese çevriliyor...`')
        video = io.BytesIO()
        video = await event.client.download_media(rep_msg.video)
        gif = await asyncio.create_subprocess_shell(
            f"ffmpeg -y -i '{video}' -vn -b:a 128k -c:a libmp3lame out.mp3")
        await gif.communicate()
        await event.edit('`Ses yükleniyor...`')
        
        try:
            await event.client.send_file(event.chat_id, "out.mp3",reply_to=rep_msg, caption='@AsenaUserBot ile sese çevrildi.')
        except:
            os.remove(video)
            return await event.edit('`Sese çevirilemedi!`')

        await event.delete()
        os.remove("out.mp3")
        os.remove(video)
    else:
        await event.edit(LANG['INVALID_COMMAND'])
        return

CmdHelp('cevir').add_command(
    'çevir foto', '<yanıt>', 'Stickeri fotoğrafa çevirir.'
).add_command(
    'çevir gif', '<yanıt>', 'Videoyu veya animasyonlu stickeri gife çevirir.'
).add_command(
    'çevir ses', '<çocuk/robot/earrape/hızlı/parazit/yankı>', 'Sese efekt uygular.'
).add_command(
    'çevir mp3', '<yanıt>', 'Yanıt verdiğiniz videoyu mp3 yapar.'
).add()