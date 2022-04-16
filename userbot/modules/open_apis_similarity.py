import aiohttp
import asyncio
import json
import os
from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp
# from userbot.language import get_value


@register(outgoing=True, pattern="^.benzerlik ?(.*)")
async def apis(event):
    degerler = event.pattern_match.group(1)

    try:
        txt = degerler.split("&&")
        if txt[1].startswith(" "):
            txt[1] = txt[1].replace(" ", "", 1)

        if len(txt) != 2:
            return await event.edit("**Girilen Cümlede 2 Adet** `&&` **Sembolü Bulundu. Lütfen** `.asena benzerlik` **Yazıp Kullanımına Göz Atın.**")

        f1 = txt[0]
        f2 = txt[1]
    except IndexError:
        return await event.edit("**Eksik Paramatreler!**\n\n**Örnek:** `benzerlik cümle1 && cümle2`")

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get('https://open-apis-rest.up.railway.app/api/similarity?text1=' + f1 + '&text2=' + f2) as response:

            html = await response.text()
            html2 = json.loads(html)
            if html2["status"] == "OK":
                sim = html2["data"]["similarity_percentage"]
                vurgu = html2["data"]["emphasis"]["emphasis"]
                sonuc = "**1. Cümle:** `" + txt[0] + "`" + "\n" + "**2. Cümle:** `" + txt[1] + "`" + "\n\n" + \
                    "**Benzerlik Oranı:** " + "`" + sim + "`" + \
                        "\n" + "**Vurgulanan Kelime:** `" + vurgu + "`"
                return await event.edit(sonuc)

            else:
                return await event.edit("__API İle İlgili Bir Sorun Var. Lütfen Destek Ekibine Bildirin.__")

Help = CmdHelp('benzerlik')
Help.add_command('benzerlik',
                 '<1. Cümle> && <2. Cümle>',
                 '2 Cümlenin Anlam Bakımından Ne Kadar Benzediğini Gösterir. (Yapay Zeka)',
                 'benzerlik Asena harika bir araç! && Asena kullanmak iyi bir seçenek!'
                 )
Help.add_info("@phaticusthiccy tarafından yapılmıştır.")
Help.add()
