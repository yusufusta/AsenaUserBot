import aiohttp
import asyncio
import json
import os
import requests
from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp
# from userbot.language import get_value

def download(url):
    response = requests.get(url)
    file = open("./tp.png", "wb")
    file.write(response.content)
    file.close()
    return True

@register(outgoing=True, pattern="^.textpro ?(.*)")
async def apis(event):
    degerler = event.pattern_match.group(1)

    try:
        txt = degerler.split()
        model = txt[0]
        text = degerler.replace(model, "")

    except IndexError:
        return await event.edit("**Eksik Paramatreler!**\n\n**Örnek:** `textpro neon Asena`\n\n__Stiller:__ `neon`, `neon2`, `devil`, `batman`, `led`, `yıldırım`, `bp`, `yaprak`, `ask`, `ask2`, `afis`, `glitch`")

    url = ""

    if model == "neon":
        url = "https://textpro.me/create-glowing-neon-light-text-effect-online-free-1061.html"
    elif model == "neon2":
        url = "https://textpro.me/neon-text-effect-online-963.html"
    elif model == "devil":
        url = "https://textpro.me/create-neon-devil-wings-text-effect-online-free-1014.html"
    elif model == "batman":
        url = "https://textpro.me/make-a-batman-logo-online-free-1066.html"
    elif model == "led":
        url = "https://textpro.me/color-led-display-screen-text-effect-1059.html"
    elif model == "yıldırım":
        url = "https://textpro.me/online-thunder-text-effect-generator-1031.html"
    elif model == "bp":
        url = "https://textpro.me/create-blackpink-logo-style-online-1001.html"
    elif model == "yaprak":
        url = "https://textpro.me/natural-leaves-text-effect-931.html"
    elif model == "ask":
        url = "https://textpro.me/free-advanced-glow-text-effect-873.html"
    elif model == "ask2":
        url = "https://textpro.me/create-neon-light-on-brick-wall-online-1062.html"
    elif model == "afis":
        url = "https://textpro.me/create-light-glow-sliced-text-effect-online-1068.html"
    elif model == "glitch":
        url = "https://textpro.me/create-impressive-glitch-text-effects-online-1027.html"

    else:
        return await event.edit("**Yanlış Paramatre!**\n\n**Örnek:** `textpro neon Asena`\n\n__Stiller:__ `neon`, `neon2`, `devil`, `batman`, `led`, `yıldırım`, `bp`, `yaprak`, `ask`, `ask2`, `afis`, `glitch`")

    await event.edit("__Fotoğraf Oluşturuluyor..__")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get('https://open-apis-rest.up.railway.app/api/textpro?url=' + url + '&text1=' + text) as response:

            html = await response.text()
            html2 = json.loads(html)
            if html2["status"] == "OK":
                img = html2["data"]
                download(img)
                await event.client.send_file(event.chat_id, './tp.png', caption="@AsenaUserBot ile Yüklendi.")
                os.remove("./tp.png")
                await event.delete()
                return True
            else:
                return await event.edit("Sunucu ile ilgili bir sorun var. Lütfen bunu destek ekibine bildirin.")

Help = CmdHelp('textpro')
Help.add_command('textpro',
                 '<stil> <metin>',
                 'Farklı Stillerde Görseller Üretir. (Tüm stilleri görmek için boş bırakın)',
                 'textpro devil phaticusthiccy'
                 )
Help.add_info("@phaticusthiccy tarafından yapılmıştır.")
Help.add()
