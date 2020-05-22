# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

""" UserBot başlangıç noktası """
import importlib
from importlib import import_module
from sqlite3 import connect
from sys import argv
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP
from .modules import ALL_MODULES
import base64

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nHATA: Girilen telefon numarası geçersiz' \
             '\n  Ipucu: Ülke kodunu kullanarak numaranı gir' \
             '\n       Telefon numaranızı tekrar kontrol edin'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()
try:
    bot.start()
    idim = bot.get_me().id
    asenabl = requests.get('https://gitlab.com/Quiec/asen/-/raw/master/asen.json').json()
    if idim in asenabl:
        bot.disconnect()

    if PLUGIN_CHANNEL_ID != None:
        print("Pluginler Yükleniyor")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
            DOGRU = 1
        except:
            KanalId = "me"
            bot.send_message("me", f"`Plugin_Channel_Id'iniz geçersiz. Pluginler kalıcı olmuyacak.`")
            DOGRU = 0

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if DOGRU == 0:
                break
            dosyaa = plugin.file.name
            print(dosyaa)
            if not os.path.exists(os.getcwd() + "/userbot/modules/" + dosyaa):
                dosya = bot.download_media(plugin, os.getcwd() + "/userbot/modules/")
            else:
                print("Bu Plugin Zaten Yüklü " + dosyaa)
                dosya = dosyaa
                break
            try:
                spec = importlib.util.spec_from_file_location(dosya, dosya)
                mod = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(mod)
            except Exception as e:
                bot.send_message(KanalId, f"`Yükleme başarısız! Plugin hatalı.\n\nHata: {e}`")
                plugin.delete()

                if os.path.exists("/userbot/modules/" + dosya):
                  os.remove(os.getcwd() + "/userbot/modules/" + dosya)
                continue
            
            ndosya = dosya.replace(".py", "")
            CMD_HELP[ndosya] = "Bu Plugin Dışarıdan Yüklenmiştir"
            bot.send_message(KanalId, f"`Plugin Yüklendi\n\Dosya: {dosya}`")
        if KanalId != "me":
            bot.send_message(KanalId, f"`Pluginler Yüklendi`")
    else:
        bot.send_message("me", f"`Lütfen pluginlerin kalıcı olması için PLUGIN_CHANNEL_ID'i ayarlayın.`")

except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Botunuz çalışıyor! Herhangi bir sohbete .alive yazarak Test edin."
          " Yardıma ihtiyacınız varsa, Destek grubumuza gelin t.me/AsenaSupport")
LOGS.info("Bot sürümünüz Asena v1.3")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
