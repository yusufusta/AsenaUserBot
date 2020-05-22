# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta
#

""" Android ile ilgili komutları içeren UserBot modülü """

import re
from requests import get
from bs4 import BeautifulSoup

from userbot import CMD_HELP
from userbot.events import register

GITHUB = 'https://github.com'
DEVICES_DATA = 'https://raw.githubusercontent.com/androidtrackers/' \
               'certified-android-devices/master/devices.json'


@register(outgoing=True, pattern="^.magisk$")
async def magisk(request):
    """ Güncel Magisk sürümleri """
    magisk_dict = {
        "Stable":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/stable.json",
        "Beta":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/beta.json",
        "Canary (Release)":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/release.json",
        "Canary (Debug)":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/debug.json"
    }
    releases = 'Güncel Magisk sürümleri:\n'
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += f'{name}: [ZIP v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | ' \
                    f'[APK v{data["app"]["version"]}]({data["app"]["link"]}) | ' \
                    f'[Uninstaller]({data["uninstaller"]["link"]})\n'
    await request.edit(releases)

@register(outgoing=True, pattern=r"^.device(?: |$)(\S*)")
async def device_info(request):
    """ Kod adı ile cihaz hakkında bilgi alın """
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text
    else:
        await request.edit("`Kullanım: .device <kod adı> / <model>`")
        return
    found = [
        i for i in get(DEVICES_DATA).json()
        if i["device"] == device or i["model"] == device
    ]
    if found:
        reply = f'{device} için arama sonuçları:\n\n'
        for item in found:
            brand = item['brand']
            name = item['name']
            codename = item['device']
            model = item['model']
            reply += f'{brand} {name}\n' \
                f'**Codename**: `{codename}`\n' \
                f'**Model**: {model}\n\n'
    else:
        reply = f"`{device} için bilgi bulunamadı!`\n"
    await request.edit(reply)


@register(outgoing=True, pattern=r"^.codename(?: |)([\S]*)(?: |)([\s\S]*)")
async def codename_info(request):
    """ Cihazın kod adını bulmak için arama yapın """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(' ')[0]
        device = ' '.join(textx.text.split(' ')[1:])
    else:
        await request.edit("`Kullanım: .codename <marka> <cihaz>`")
        return
    found = [
        i for i in get(DEVICES_DATA).json()
        if i["brand"].lower() == brand and device in i["name"].lower()
    ]
    if len(found) > 8:
        found = found[:8]
    if found:
        reply = f'{brand.capitalize()} {device.capitalize()} için arama sonuçları:\n\n'
        for item in found:
            brand = item['brand']
            name = item['name']
            codename = item['device']
            model = item['model']
            reply += f'{brand} {name}\n' \
                f'**Codename**: `{codename}`\n' \
                f'**Model**: {model}\n\n'
    else:
        reply = f"`{device} için kod adı bulunamadı!`\n"
    await request.edit(reply)


@register(outgoing=True, pattern=r"^.specs(?: |)([\S]*)(?: |)([\s\S]*)")
async def devices_specifications(request):
    """ Mobil cihaz özellikleri """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(' ')[0]
        device = ' '.join(textx.text.split(' ')[1:])
    else:
        await request.edit("`Kullanım: .specs <marka> <cihaz>`")
        return
    all_brands = BeautifulSoup(
        get('https://www.devicespecifications.com/tr/brand-more').content,
        'lxml').find('div', {
            'class': 'brand-listing-container-news'
        }).findAll('a')
    brand_page_url = None
    try:
        brand_page_url = [
            i['href'] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        await request.edit(f'`{brand} bilinmeyen marka!`')
    devices = BeautifulSoup(get(brand_page_url).content, 'lxml') \
        .findAll('div', {'class': 'model-listing-container-80'})
    device_page_url = None
    try:
        device_page_url = [
            i.a['href']
            for i in BeautifulSoup(str(devices), 'lxml').findAll('h3')
            if device in i.text.strip().lower()
        ]
    except IndexError:
        await request.edit(f"`{device} bulunamadı!`")
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ''
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, 'lxml')
        reply = '\n**' + info.title.text.split('-')[0].strip() + '**\n\n'
        info = info.find('div', {'id': 'model-brief-specifications'})
        specifications = re.findall(r'<b>.*?<br/>', str(info))
        for item in specifications:
            title = re.findall(r'<b>(.*?)</b>', item)[0].strip()
            data = re.findall(r'</b>: (.*?)<br/>', item)[0]\
                .replace('<b>', '').replace('</b>', '').strip()
            reply += f'**{title}**: {data}\n'
    await request.edit(reply)


@register(outgoing=True, pattern=r"^.twrp(?: |$)(\S*)")
async def twrp(request):
    """ Android cihazlar için TWRP """
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(' ')[0]
    else:
        await request.edit("`Kullanım: .twrp <kod adı>`")
        return
    url = get(f'https://dl.twrp.me/{device}/')
    if url.status_code == 404:
        reply = f"`{device} için resmi twrp bulunamadı!`\n"
        await request.edit(reply)
        return
    page = BeautifulSoup(url.content, 'lxml')
    download = page.find('table').find('tr').find('a')
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = f'**{device} için güncel twrp:**\n' \
        f'[{dl_file}]({dl_link}) - __{size}__\n' \
        f'**Güncelleme tarihi:** __{date}__\n'
    await request.edit(reply)


CMD_HELP.update({
    "android":
    ".magisk\
\nGüncel Magisk sürümleri\
\n\n.device <kod adı>\
\nKullanım: Android cihazı hakkında bilgi\
\n\n.codename <marka> <cihaz>\
\nKullanım: Android cihaz kod adlarını arayın.\
\n\n.specs <marka> <cihaz>\
\nKullanım: Cihaz özellikleri hakkında bilgi alın.\
\n\n.twrp <kod adı>\
\nKullanım: Hedeflenen cihaz için resmi olan güncel twrp sürümlerini alın."
})
