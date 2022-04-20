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
    file = open("./avatar.jpg", "wb")
    file.write(response.content)
    file.close()
    return True

@register(outgoing=True, pattern="^.game ?(.*)")
async def apis(event):
    degerler = event.pattern_match.group(1)

    try:
        txt = degerler.split()
        game_old = txt[0]
        game = degerler
    except IndexError:
        return await event.edit("**Eksik Paramatreler!**\n\n**Örnek:** `game genshin`")

    await event.edit("__" + game + " Adlı oyunun sistem gereksinimleri toplanıyor..__")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get('https://open-apis-rest.up.railway.app/api/game_specs?game=' + game) as response:

            html = await response.text()
            html2 = json.loads(html)
            if html2["status"] == "OK":

                name = html2["data"]["game"]["name"]
                release_date = html2["data"]["game"]["release_date"]
                genre = html2["data"]["game"]["genre"]
                dev = html2["data"]["game"]["developer"]
                owner = html2["data"]["game"]["publisher"]
                avatar = html2["data"]["game"]["avatar"]

                sy_min_cpu = html2["data"]["system_requirements"]["minimum"]["cpu"]
                sy_min_gpu = html2["data"]["system_requirements"]["minimum"]["gpu"]
                sy_min_ram = html2["data"]["system_requirements"]["minimum"]["ram"]
                sy_min_hdd = html2["data"]["system_requirements"]["minimum"]["hdd"]
                sy_min_drx = html2["data"]["system_requirements"]["minimum"]["directx"]
                sy_min_os = html2["data"]["system_requirements"]["minimum"]["os"]

                sy_rc_cpu = html2["data"]["system_requirements"]["recommended"]["cpu"]
                sy_rc_gpu = html2["data"]["system_requirements"]["recommended"]["gpu"]
                sy_rc_ram = html2["data"]["system_requirements"]["recommended"]["ram"]
                sy_rc_hdd = html2["data"]["system_requirements"]["recommended"]["hdd"]
                sy_rc_drx = html2["data"]["system_requirements"]["recommended"]["directx"]
                sy_rc_os = html2["data"]["system_requirements"]["recommended"]["os"]

                popularity = html2["data"]["reviews"]["popularity"]
                graphics = html2["data"]["reviews"]["graphics"]
                design = html2["data"]["reviews"]["design"]
                gameplay = html2["data"]["reviews"]["gameplay"]
                sound = html2["data"]["reviews"]["sound"]
                music = html2["data"]["reviews"]["music"]
                innovations = html2["data"]["reviews"]["innovations"]
                overall = html2["data"]["reviews"]["overall"]

                download(avatar)
                await event.client.send_file(
                    event.chat_id, './avatar.png',
                    caption="__Oyun:__ " + name +
                    "\n__Yayın Tarihi:__ " + release_date +
                    "\n__Tür:__ " + genre +
                    "\n__Geliştirici:__ " + dev +
                    "\n__Sahip Firma:__ " + owner +
                    "\n\n**Minimum Sistem Gereksinimleri:**" +
                    "\n__CPU:__ " + sy_min_cpu +
                    "\n__GPU:__ " + sy_min_gpu +
                    "\n__RAM:__ " + sy_min_ram +
                    "\n__HDD:__ " + sy_min_hdd +
                    "\n__DirectX:__ " + sy_min_drx +
                    "\n__OS:__ " + sy_min_os +
                    "\n\n**Önerilen Sistem Gereksinimleri:**" +
                    "\n__CPU:__ " + sy_rc_cpu +
                    "\n__GPU:__ " + sy_rc_gpu +
                    "\n__RAM:__ " + sy_rc_ram +
                    "\n__HDD:__ " + sy_rc_hdd +
                    "\n__DirectX:__ " + sy_rc_drx +
                    "\n__OS:__ " + sy_rc_os +
                    "\n\n**İncelemeler:**" +
                    "\n__Popülerite:__ " + popularity +
                    "\n__Grafik:__ " + graphics +
                    "\n__Dizayn:__ " + design +
                    "\n__Oynanış:__ " + gameplay +
                    "\n__Ses:__ " + sound +
                    "\n__Müzik:__ " + music +
                    "\n__Yenilik:__ " + innovations +
                    "\n__Genel:__ " + overall
                )
                os.remove("./avatar.png")
                await event.delete()
            else:
                return await event.edit("__" + game + " Adında bir oyun bulunamadı.__")

Help = CmdHelp('game')
Help.add_command('game',
                 '<oyun adı>',
                 'Oyunun Sistem Gereksinimlerini Gösterir.',
                 'game genshin'
                 )
Help.add_info("@phaticusthiccy tarafından yapılmıştır.")
Help.add()
