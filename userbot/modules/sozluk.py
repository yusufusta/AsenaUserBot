# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

# Turkish word meaning. Only Turkish. Coded @By_Azade, Seden uyarlaması @qulec
#

import requests

from userbot import CMD_HELP
from userbot.events import register
from userbot.modules.admin import get_user_from_event

from html.parser import HTMLParser
from bs4 import BeautifulSoup

def searchTureng_tr(word):
    url="https://tureng.com/tr/turkce-ingilizce/"+word
    try:
        answer =  requests.get(url)
    except:
        return "No connection"
    soup = BeautifulSoup(answer.content, 'html.parser')
    trlated='{} Kelimesinin Anlamı/Anlamları:\n\n'.format(word)
    try:
        table = soup.find('table')
        td = table.find_all('td', attrs={'lang':'en'})
        # print(td)
        for val in td[0:5]:
            trlated = '{}👉  {}\n'.format(trlated , val.text )
        return trlated
    except:
        return "Sonuç bulunamadı"

@register(outgoing=True, pattern="^.tureng ?(.*)")
async def tureng(event): 
    input_str = event.pattern_match.group(1)
    result = searchTureng_tr(input_str)
    await event.edit(result)

@register(outgoing=True, pattern="^.tdk ?(.*)")
async def tdk(event): 
    if event.fwd_from:
        return
    inp = event.pattern_match.group(1)
    kelime = "https://sozluk.gov.tr/gts?ara={}".format(inp)
    headers = {"USER-AGENT": "Seden"}
    response = requests.get(kelime, headers=headers).json()
    
    try:
        anlam_sayisi = response[0]['anlam_say']
        x = "TDK Sözlük\n\nKelime: **{}**\n".format(inp)
        for anlamlar in range(int(anlam_sayisi)):
            x += "👉{}\n".format(response[0]['anlamlarListe'][anlamlar]['anlam'])
            # print(x)
        await event.edit(x)
    except KeyError:
        await event.edit("`Kelime bulunamadı`")

CMD_HELP.update({
    "sozluk":
    ".tdk <kelime> .\
    \nKullanım: Verdiğiniz kelimeyi TDK Sözlükte arar.\n\n.tureng <kelime> .\
    \nKullanım: Verdiğiniz kelimeyi Tureng Sözlükte arar."
})
