import aiohttp
import requests
import asyncio
import json
import os
from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp
# from userbot.language import get_value


@register(outgoing=True, pattern="^.tiktok ?(.*)")
async def apis(event):
    degerler = event.pattern_match.group(1)

    try:
        txt = degerler.split()
        url = txt[0]
    except IndexError:
        return await event.edit("**Lütfen Bir Tiktok Bağlantısı Girin!**")

    await event.edit("__Video İndiriliyor..__")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get('https://open-apis-rest.up.railway.app/api/tiktok?url=' + url) as response:

            html = await response.text()
            html2 = json.loads(html)
            if html2["status"] == "OK":
                vid = html2["data"]["server1"]["video"]
                resp = requests.get(vid)
                with open("./tt.mp4", "wb") as f:
                    f.write(resp.content)

                await event.client.send_file(event.chat_id, './tt.mp4', caption="@AsenaUserBot ile Yüklendi.")
                os.remove("./tt.mp4")
                await event.delete()
                return True
            else:
                return await event.edit("Lütfen Bağlantınızı Kontrol Edin. Sorun hala devam ediyorsa destek ekibine ulaşın.")

Help = CmdHelp('tiktok')
Help.add_command('tiktok',
                 '<tiktok url>',
                 'Tiktok üzerinden video indirir.',
                 'tiktok https://vm.tiktok.com/ZSeKGPhsV'
                 )
Help.add_info("@phaticusthiccy tarafından yapılmıştır.")
Help.add()
