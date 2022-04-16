# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta
#

""" UserBot yardım komutu """

from userbot.cmdhelp import CmdHelp
from userbot import cmdhelp
from userbot import CMD_HELP
from userbot.events import register
import aiohttp
import asyncio
import json
import os
from googletrans import LANGUAGES, Translator
translator = Translator(service_urls=[
      'translate.google.cn',
])
from emoji import get_emoji_regexp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__asena")

# ████████████████████████████████ #

def deEmojify(inputString):
    """ Emojileri ve diğer güvenli olmayan karakterleri metinden kaldırır. """
    return get_emoji_regexp().sub(u'', inputString)


@register(outgoing=True, pattern="^.asena(?: |$)(.*)")
async def asena(event):
    """ .asena komutu için """
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit(LANG["NEED_PLUGIN"])
    else:
        string = ""
        sayfa = [sorted(list(CMD_HELP))[i:i + 5] for i in range(0, len(sorted(list(CMD_HELP))), 5)]
        
        for i in sayfa:
            string += f'`▶️ `'
            for sira, a in enumerate(i):
                string += "`" + str(a)
                if sira == i.index(i[-1]):
                    string += "`"
                else:
                    string += "`, "
            string += "\n"
        await event.edit(LANG["NEED_MODULE"] + '\n\n' + string)



BOT = "N"

@register(outgoing=True, pattern="^.chatbot ?(.*)")
async def asena(event):
    global BOT
    if (event.pattern_match.group(1) == "on" or event.pattern_match.group(1) == "aç" or event.pattern_match.group(1) == "ac"):
        if BOT == "Y":
            return await event.edit("**Chatbot Halihazırda Açık!**")

        BOT = "Y"
        await event.edit("**Asena Yapay Zeka ChatBot Açıldı!**\n**Kullanmak için cümleye** `Asena` **ile başlayın.**")
    elif (event.pattern_match.group(1) == "off" or event.pattern_match.group(1) == "kapa" or event.pattern_match.group(1) == "kapat"):
        if BOT == "N":
            return await event.edit("**Chatbot Halihazırda Kapalı!**")

        BOT = "N"
        await event.edit("**Asena Yapay Zeka ChatBot Kapandı!**")
    else:
        await event.edit("**Eksik Parametreler!** \n`.asena chatbot` **Komutunu kullanarak talimatları okuyun.**")



@register(outgoing=True, disable_edited=False)
async def txt(msg):
    global BOT
    if msg.chat_id == -1001420605284:
        return False
    if msg.chat_id == -1001363514260:
        return False

    if BOT == "Y":
        message = msg.raw_text
        user_id = msg.sender.id
        if message.startswith("asena") or message.startswith("Asena"):
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                aftext = translator.translate(deEmojify(message), dest="en")
                async with session.get('https://open-apis-rest.up.railway.app/api/chatbot?id=' + str(user_id) + f"&message={aftext.text}") as response:
                
                    html = await response.text()
                    html2 = json.loads(html)
                    if html2["status"] == "OK":
                        outtext = translator.translate(html2["data"], dest="tr")
                        await msg.client.send_message(msg.chat_id, f"{outtext.text}", reply_to=msg, link_preview=False)
                    else:
                        if "Message" in html2["error"]:
                            return await msg.edit("__Seni anlamam için birşeyler yazmalısın..__")

        else:
            return False
    else:
	    return False



Help = CmdHelp('chatbot')
Help.add_command('chatbot', 
    '<on / off veya ac / kapa>', 
    'Yapay Zeka Sohbet Botunu Aktif Eder.',
    'chatbot on \nchatbot off'
)
Help.add_info("@phaticusthiccy tarafından yapılmıştır.")
Help.add()