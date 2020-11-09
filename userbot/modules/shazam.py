# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta
# Telegram @Fusuf

# Coded by @Fusuf

from pydub import AudioSegment
from json import dumps
from userbot.events import register
from .shazam_helper.communication import recognize_song_from_signature
from .shazam_helper.algorithm import SignatureGenerator
from requests import get
from os import remove
import urllib.parse
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.shazam")
async def shazam(event):
    if not event.is_reply:
        return await event.edit('`Lütfen bir ses dosyasına yanıt verin!`')
    else:
        await event.edit('`⬇️ Ses dosyası indiriliyor...`')
        reply_message = await event.get_reply_message()
        dosya = await reply_message.download_media()

        await event.edit('`🛠 Ses dosyası fingerprint formatına çeviriliyor...`')
        audio = AudioSegment.from_file(dosya)
        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
            
        signature_generator = SignatureGenerator()
        signature_generator.feed_input(audio.get_array_of_samples())
            
        signature_generator.MAX_TIME_SECONDS = 12
        if audio.duration_seconds > 12 * 3:
            signature_generator.samples_processed += 16000 * (int(audio.duration_seconds / 2) - 6)
            
        results = '{"error": "Not found"}'
        sarki = None
        await event.edit('`🎧 🎤 Shazamlanıyor...`')
        while True:
            signature = signature_generator.get_next_signature()
            if not signature:
                sarki = results
                break
            results = recognize_song_from_signature(signature)
            if results['matches']:
                sarki = results
                break
            else:
                await event.edit(f'`İlk {(signature_generator.samples_processed / 16000)} saniyede hiçbir şey bulunamadı... Biraz daha deniyorum.`')
        
        if not 'track' in sarki:
            return await event.edit('`Üzgünüm Shazam verdiniğiniz sesi anlamadı 😔. Biraz daha açık ses iletir misiniz?`')
        await event.edit('`✅ Şarkıyı buldum... Bilgiler getiriliyor...`')
        Caption = f'**Şarkı:** [{sarki["track"]["title"]}]({sarki["track"]["url"]})\n'
        if 'artists' in sarki['track']:
            Caption += f'**Sanatçı(lar):** [{sarki["track"]["subtitle"]}](https://www.shazam.com/artist/{sarki["track"]["artists"][0]["id"]})\n'
        else:
            Caption += f'**Sanatçı(lar):** `{sarki["track"]["subtitle"]}`\n'

        if 'genres'in sarki['track']:
            Caption += f'**Tür:** `{sarki["track"]["genres"]["primary"]}`\n'

        if sarki["track"]["sections"][0]["type"] == "SONG":
            for metadata in sarki["track"]["sections"][0]["metadata"]:
                Caption += f'**{"Yıl" if metadata["title"] == "Sorti" else metadata["title"]}:** `{metadata["text"]}`\n'

        Caption += '\n**Müzik Platformları:** '
        for provider in sarki['track']['hub']['providers']:
            if provider['actions'][0]['uri'].startswith('spotify:track'):
                Url = provider['actions'][0]['uri'].replace(
                    'spotify:track:', 'http://open.spotify.com/track/'
                )
            elif provider['actions'][0]['uri'].startswith('intent:#Intent;action=android.media.action.MEDIA_PLAY_FROM_SEARCH'):
                Url = f'https://open.spotify.com/search/' + urllib.parse.quote(sarki["track"]["subtitle"] + ' - ' + sarki["track"]["title"])
            elif provider['actions'][0]['uri'].startswith('deezer'):
                Url = provider['actions'][0]['uri'].replace(
                    'deezer-query://', 'https://'
                )
            else:
                Url = provider['actions'][0]['uri']
            Caption += f'[{provider["type"].capitalize()}]({Url}) '
        for section in sarki['track']['sections']:
            if section['type'] == 'VIDEO':
                if 'youtubeurl' in section:
                    Youtube = get(section['youtubeurl']).json()
                else:
                    return

                Caption += f'\n**Klip Videosu:** [Youtube]({Youtube["actions"][0]["uri"]})'

        if 'images' in sarki["track"] and len(sarki["track"]["images"]) >= 1:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                sarki["track"]["images"]["coverarthq"] if 'coverarthq' in sarki["track"]["images"] else sarki["track"]["images"]["background"],
                caption=Caption,
                reply_to=reply_message
                )
        else:
            await event.edit(Caption)  
        remove(dosya)

CmdHelp('shazam').add_command(
    'shazam', '<yanıt>', 'Yanıt verdiğiniz ses dosyasını Shazamda arar.'
).add()