# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

from asyncio import sleep
from json import loads
from json.decoder import JSONDecodeError
from os import (environ, path, remove)
from sys import setrecursionlimit

import spotify_token as st
from requests import (get, post)
from telethon import events
from telethon.errors import AboutTooLongError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateProfileRequest

from userbot import (BIO_PREFIX, BOTLOG, BOTLOG_CHATID, CMD_HELP, DEFAULT_BIO,
                     SPOTIFY_DC, SPOTIFY_KEY, bot)
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from telegraph import Telegraph
telegraph = Telegraph()

# =================== CONSTANT ===================
# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("spotify")

# ████████████████████████████████ #

SPO_BIO_ENABLED = LANG['BIO_ENABLED']
SPO_BIO_DISABLED = LANG['BIO_DISABLED']
SPO_BIO_RUNNING = LANG['BIO_RUNNING']
ERROR_MSG = LANG['ERROR']

USERNAME = SPOTIFY_DC
PASSWORD = SPOTIFY_KEY

ARTIST = 0
SONG = 0

BIOPREFIX = BIO_PREFIX

SPOTIFYCHECK = False
RUNNING = False
OLDEXCEPT = False
PARSE = False


# ================================================
async def get_spotify_token():
    sptoken = st.start_session(USERNAME, PASSWORD)
    access_token = sptoken[0]
    environ["spftoken"] = access_token


async def update_spotify_info():
    global ARTIST
    global SONG
    global PARSE
    global SPOTIFYCHECK
    global RUNNING
    global OLDEXCEPT
    oldartist = ""
    oldsong = ""
    while SPOTIFYCHECK:
        try:
            RUNNING = True
            spftoken = environ.get("spftoken", None)
            hed = {'Authorization': 'Bearer ' + spftoken}
            url = 'https://api.spotify.com/v1/me/player/currently-playing'
            response = get(url, headers=hed)
            data = loads(response.content)
            artist = data['item']['album']['artists'][0]['name']
            song = data['item']['name']
            OLDEXCEPT = False
            oldsong = environ.get("oldsong", None)
            if song != oldsong and artist != oldartist:
                oldartist = artist
                environ["oldsong"] = song
                spobio = BIOPREFIX + " 🎧: " + artist + " - " + song
                try:
                    await bot(UpdateProfileRequest(about=spobio))
                except AboutTooLongError:
                    short_bio = "🎧: " + song
                    await bot(UpdateProfileRequest(about=short_bio))
                environ["errorcheck"] = "0"
        except KeyError:
            print(2)

            errorcheck = environ.get("errorcheck", None)
            if errorcheck == 0:
                await update_token()
            elif errorcheck == 1:
                SPOTIFYCHECK = False
                await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                print(ERROR_MSG)
                if BOTLOG:
                    await bot.send_message(BOTLOG_CHATID, ERROR_MSG)
        except JSONDecodeError:
            print(3)
            OLDEXCEPT = True
            await sleep(6)
            await bot(UpdateProfileRequest(about=DEFAULT_BIO))
        except TypeError:
            print(4)
            await dirtyfix()
        except Exception as e:
            print(e)
        SPOTIFYCHECK = False
        await sleep(2)
        await dirtyfix()
    RUNNING = False


async def update_token():
    sptoken = st.start_session(USERNAME, PASSWORD)
    access_token = sptoken[0]
    environ["spftoken"] = access_token
    environ["errorcheck"] = "1"
    await update_spotify_info()


async def dirtyfix():
    global SPOTIFYCHECK
    SPOTIFYCHECK = True
    await sleep(4)
    await update_spotify_info()


@register(outgoing=True, pattern="^.spotify aç$")
async def set_biostgraph(setstbio):
    setrecursionlimit(700000)
    if not SPOTIFYCHECK:
        environ["errorcheck"] = "0"
        await setstbio.edit(SPO_BIO_ENABLED)
        await get_spotify_token()
        await dirtyfix()
    else:
        await setstbio.edit(SPO_BIO_RUNNING)


@register(outgoing=True, pattern="^.spotify kapa$")
async def set_biodgraph(setdbio):
    global SPOTIFYCHECK
    global RUNNING
    SPOTIFYCHECK = False
    RUNNING = False
    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
    await setdbio.edit(SPO_BIO_DISABLED)



def msToStr(time):
    seconds = round((time/1000)%60)
    minutes = int((time/(1000*60))%60)
    text = str(minutes)+":"
    if seconds < 10:
        text += "0"+str(seconds)
    else:
        text += str(seconds)
    return text

def generatePlayerStr(now, time):
    string = "─"
    arr = []
    for _ in range(0, 18):
        arr.append(string)
    index = int((now*18)/time)
    if index >= len(arr):
        index = len(arr)-1
    arr[index] = '⚪'
    return ("".join(arr))

def get_spotify_info(TIME=5):
    try:
        spftoken = environ.get("spftoken", None)
        hed = {'Authorization': 'Bearer ' + spftoken}
        url = 'https://api.spotify.com/v1/me/player/currently-playing'
        response = get(url, headers=hed)
        data = loads(response.content)
        item = data['item']
        artistsStr = "" 
        artists = []
        if len(item['artists']) > 0:
            for i in item['artists']:
                artists.append(str(i['name']))
            artistsStr = ", ".join(artists)
            artistsStr = "\n__"+artistsStr+"__"
        song = f"**{item['name']}**"
        songinfo = song + artistsStr
        name = item['name'] + " - "+(", ".join(artists))
        image = "🔄"
        try:
            url = item['external_urls']['spotify']
            url = f"[Spotify'da Aç]({url})"
        except Exception:
            url = "𝘴𝘱𝘰𝘵𝘪𝘧𝘺 𝘯𝘰𝘸 𝘱𝘭𝘢𝘺𝘪𝘯𝘨"  
        nowtime = int(data['progress_ms'])
        totaltime = int(item['duration_ms'])
        if len(item['album']['images']) > 0:
            telegraph.create_account(short_name='spotify')
            if path.exists("@AsenaUserBot-Spotify.jpg"):
                remove("@AsenaUserBot-Spotify.jpg")          
            try:
                r = get(str(item['album']['images'][0]['url']))
                with open("@AsenaUserBot-Spotify.jpg", 'wb') as f:
                    f.write(r.content)    

                with open('@AsenaUserBot-Spotify.jpg', 'rb') as f:
                    req = post('https://telegra.ph/upload', 
                    files={'Hey': ('Hey', f, 'image/jpeg')}  # image/gif, image/jpeg, image/jpg, image/png, video/mp4
                    ).json()
                    image = "[🔄](https://telegra.ph"+req[0]['src']+")"
            except Exception:
                pass
        if path.exists("@AsenaUserBot-Spotify.jpg"):
            remove("@AsenaUserBot-Spotify.jpg") 
        art = []
        message = ""
        Stop = False
        for _ in range(0, TIME):       
            nowstr = msToStr(nowtime)
            totalstr = msToStr(totaltime)
            progress = generatePlayerStr(nowtime, totaltime)
            mp = progress+"\n\n◄◄⠀▐▐ ⠀►►⠀⠀⠀ "+nowstr+" / "+totalstr + f"⠀⠀⠀{image}🔀\n\n{url}"
            if message == "":
                message = mp
            appendstr = songinfo + "\n\n" + mp
            if appendstr not in art:
                art.append(appendstr)
            nowtime += 1000
            if nowtime > totaltime:
                nowtime = totaltime
                Stop = True
            elif Stop is True or nowstr == totalstr:
                break
        arr = [message, name, art]
        return arr       
    except KeyError:
        print(2)
        return LANG['ERROR_NP'] 
    except JSONDecodeError:
        print(3)
        return LANG['NP_NONE'] 
    except TypeError:
        print(4)
        return LANG['ERROR_NP']  
    except Exception as e:
        print(e)
        return LANG['ERROR_NP'] 


  
@register(outgoing=True, pattern="^.snp (.*)")
@register(outgoing=True, pattern="^.snp$")
@register(outgoing=True, pattern="^.spotify np$")
@register(outgoing=True, pattern="^.spotify np (.*)")
async def nowplaying(event):
    ANIMTIME = 5
    try:
        arg = event.pattern_match.group(1)
        if len(arg) > 0 and int(arg) > 0:
            ANIMTIME = int(arg)
    except Exception:
        pass
        
    await event.edit(LANG['NP_GET'])
    try:
        await get_spotify_token()
    except Exception:
        return await event.edit(LANG['ERROR_TOKEN']) 
    info = get_spotify_info(ANIMTIME)
    if isinstance(info, list) is False:
        await event.edit(info)
    else:
        msg = info[2]
        for item in enumerate(msg):
            await event.edit(item[1], link_preview=True)
            await sleep(1)
                    
@register(outgoing=True, pattern="^.smp3$")
@register(outgoing=True, pattern="^.spotify mp3$")
async def getmp3(event):
    await event.edit(LANG['NP_GET'])
    try:
        await get_spotify_token()
    except Exception:
        return await event.reply(LANG['ERROR_TOKEN'])
    info = get_spotify_info()
    if isinstance(info, list) is False:
        await event.edit(info)
    else:
        msg = info[0]      
        songinfo = info[1]         
        msgs = info[2]
        try:
            chat = "@DeezerMusicBot"
            async with bot.conversation(chat) as conv:
                try:     
                    await conv.send_message(songinfo)
                except YouBlockedUserError:
                    return
                sarkilar = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
                await event.client.send_read_acknowledge(conv.chat_id)
                if sarkilar.audio:
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await event.client.send_message(event.chat_id, msg, file=sarkilar.message)
                    await event.delete()
                elif sarkilar.buttons[0][0].text == "No results":
                    for item in enumerate(msgs):
                        await event.edit(item[1], link_preview=True)
                        await sleep(1)
                    return
                else:
                    await sarkilar.click(0)
                    sarki = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await event.client.send_message(event.chat_id, msg, file=sarki.message)
                    await event.delete()
        except Exception as e:
            print(e)
            for item in enumerate(msgs):
                await event.edit(item[1], link_preview=True)
                await sleep(1)

CmdHelp('spotify').add_command(
    'spotify aç', None, 'Spotify bio aktifleştirir.'
).add_command(
    'spotify kapa', None, 'Spotify bio devredışı bırakır.'
).add_command(
    'spotify np', '<animasyon süre = 5>', "Süre kadar player animasyonlu şekilde Spotify'da çalan şarkınızı gösterir. (Kısaltma komut: .snp)"
).add_command(
    'spotify mp3', None, "Spotify'da çalan şarkınızı deezer botunda bulup ascii art haliyle gönderir. (Kısaltma komut: .smp3)"
).add()