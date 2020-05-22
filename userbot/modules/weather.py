# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


"""Bir bölgenin hava durumunu gösterir."""

import json
from requests import get
from datetime import datetime
from pytz import country_timezones as c_tz
from pytz import timezone as tz
from pytz import country_names as c_n

from userbot import CMD_HELP, WEATHER_DEFCITY
from userbot import OPEN_WEATHER_MAP_APPID as OWM_API
from userbot.events import register

# ===== CONSTANT =====
if WEATHER_DEFCITY:
    DEFCITY = WEATHER_DEFCITY
else:
    DEFCITY = None
# ====================


async def get_tz(con):
    """ Verilen ülkenin zaman dilimini alır. """
    """ @aragon12 ve @zakaryan2004'e teşekkürler. """
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


@register(outgoing=True, pattern="^.weather(?: |$)(.*)")
async def get_weather(weather):
    """ .weather komutu bir bölgenin hava durumunu OpenWeatherMap üzerinden alır. """

    if not OWM_API:
        await weather.edit(
            "`Önce` https://openweathermap.org/ `adresinden bir API anahtarı almalısın.`")
        return

    APPID = OWM_API

    if not weather.pattern_match.group(1):
        CITY = DEFCITY
        if not CITY:
            await weather.edit(
                "`WEATHER_DEFCITY değişkeniyle bir şehri varsayılan olarak belirt, ya da komutu yazarken hangi şehrin hava durumunu istediğini de belirt!`"
            )
            return
    else:
        CITY = weather.pattern_match.group(1)

    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items() for timezone in timezones
    }

    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f'{country}']
            except KeyError:
                await weather.edit("`Geçersiz ülke.`")
                return
            CITY = newcity[0].strip() + "," + countrycode.strip()

    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}'
    request = get(url)
    result = json.loads(request.text)

    if request.status_code != 200:
        await weather.edit(f"`Geçersiz ülke.`")
        return

    cityname = result['name']
    curtemp = result['main']['temp']
    humidity = result['main']['humidity']
    min_temp = result['main']['temp_min']
    max_temp = result['main']['temp_max']
    desc = result['weather'][0]
    desc = desc['main']
    country = result['sys']['country']
    sunrise = result['sys']['sunrise']
    sunset = result['sys']['sunset']
    wind = result['wind']['speed']
    winddir = result['wind']['deg']

    ctimezone = tz(c_tz[country][0])
    time = datetime.now(ctimezone).strftime("%A, %I:%M %p")
    fullc_n = c_n[f"{country}"]

    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    div = (360 / len(dirs))
    funmath = int((winddir + (div / 2)) / div)
    findir = dirs[funmath % len(dirs)]
    kmph = str(wind * 3.6).split(".")
    mph = str(wind * 2.237).split(".")

    def fahrenheit(f):
        temp = str(((f - 273.15) * 9 / 5 + 32)).split(".")
        return temp[0]

    def celsius(c):
        temp = str((c - 273.15)).split(".")
        return temp[0]

    def sun(unix):
        xx = datetime.fromtimestamp(unix, tz=ctimezone).strftime("%I:%M %p")
        return xx

    await weather.edit(
        f"**Sıcaklık:** `{celsius(curtemp)}°C | {fahrenheit(curtemp)}°F`\n"
        +
        f"**En Düşük Sıcaklık:** `{celsius(min_temp)}°C | {fahrenheit(min_temp)}°F`\n"
        +
        f"**En Yüksek Sıcaklık:** `{celsius(max_temp)}°C | {fahrenheit(max_temp)}°F`\n"
        + f"**Nem:** `{humidity}%`\n" +
        f"**Rüzgar Hızı:** `{kmph[0]} kmh | {mph[0]} mph, {findir}`\n" +
        f"**Gündoğumu:** `{sun(sunrise)}`\n" +
        f"**Günbatımı:** `{sun(sunset)}`\n\n" + f"**{desc}**\n" +
        f"`{cityname}, {fullc_n}`\n" + f"`{time}`")


CMD_HELP.update({
    "weather":
    "Kullanım: .weather şehir adı veya .weather şehir adı, ülke adı/ülke kodu\
    \nBir bölgenin hava durumunu verir."
})
