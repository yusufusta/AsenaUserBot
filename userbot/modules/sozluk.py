# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

# Turkish word meaning. Only Turkish. Coded @By_Azade, Asena uyarlaması @qulec
#

import requests

from userbot import CMD_HELP
from userbot.events import register
from bs4 import BeautifulSoup
import os
from json import loads
from userbot.cmdhelp import CmdHelp

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

def getSimilarWords(kelime, limit = 5):
    benzerler = []
    if not os.path.exists('autocomplete.json'):
        words = requests.get(f'https://sozluk.gov.tr/autocomplete.json')
        open('autocomplete.json', 'a+').write(words.text)
        words = words.json()
    else:
        words = loads(open('autocomplete.json', 'r').read())

    for word in words:
        if word['madde'].startswith(kelime) and not word['madde'] == kelime:
            if len(benzerler) > limit:
                break
            benzerler.append(word['madde'])
    benzerlerStr = ""
    for benzer in benzerler:
        if not benzerlerStr == "":
            benzerlerStr += ", "
        benzerlerStr += f"`{benzer}`"
    return benzerlerStr
    
@register(outgoing=True, pattern="^.tdk ?(.*)")
async def tdk(event): 
    inp = event.pattern_match.group(1)
    await event.edit('**Bekle!**\n__Sözlükte arıyorum...__')
    response = requests.get(f'https://sozluk.gov.tr/gts?ara={inp}').json()
    if 'error' in response:
        await event.edit(f'**Kelimeniz({inp}) Büyük Türkçe Sözlük\'te Bulunamadı!**')
        words = getSimilarWords(inp)
        if not words == '':
            return await event.edit(f'__Kelimeniz({inp}) Büyük Türkçe Sözlük\'te Bulunamadı!__\n\n**Benzer Kelimeler:** {words}')
    else:
        anlamlarStr = ""
        for anlam in response[0]["anlamlarListe"]:
            anlamlarStr += f"\n**{anlam['anlam_sira']}.**"
            if ('ozelliklerListe' in anlam) and ((not anlam["ozelliklerListe"][0]["tam_adi"] == None) or (not anlam["ozelliklerListe"][0]["tam_adi"] == '')):
                anlamlarStr += f"__({anlam['ozelliklerListe'][0]['tam_adi']})__"
            anlamlarStr += f' ```{anlam["anlam"]}```'

            if response[0]["cogul_mu"] == '0':
                cogul = '❌'
            else:
                cogul = '✅'
            
            if response[0]["ozel_mi"] == '0':
                ozel = '❌'
            else:
                ozel = '✅'


        await event.edit(f'**Kelime:** `{inp}`\n\n**Çoğul Mu:** {cogul}\n**Özel Mi:** {ozel}\n\n**Anlamlar:**{anlamlarStr}')
        words = getSimilarWords(inp)
        if not words == '':
            return await event.edit(f'**Kelime:** `{inp}`\n\n**Çoğul Mu:** `{cogul}`\n**Özel Mi:** {ozel}\n\n**Anlamlar:**{anlamlarStr}' + f'\n\n**Benzer Kelimeler:** {words}')

CmdHelp('sozluk').add_command(
    'tdk', '<kelime>', 'Verdiğiniz kelimeyi TDK Sözlükte arar.'
).add_command(
    'tureng', '<kelime>', 'Verdiğiniz kelimeyi Tureng Sözlükte arar.'
).add()