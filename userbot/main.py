# Copyright (C) 2020 TeamDerUntergang.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

""" UserBot başlangıç noktası """
import importlib
from importlib import import_module
from sqlite3 import connect
from sys import argv
import os

from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID
from .modules import ALL_MODULES

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
    if PLUGIN_CHANNEL_ID != None:
        print("Pluginler Yükleniyor")
        for plugin in bot.iter_messages(PLUGIN_CHANNEL_ID, filter=InputMessagesFilterDocument):
            dosya = bot.download_media(plugin, os.getcwd() + "/userbot/modules/")
            try:
                spec = importlib.util.spec_from_file_location(dosya, dosya)
                mod = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(mod)
            except Exception as e:
                bot.send_message("me", f"`Yükleme başarısız! Plugin hatalı.\n\nHata: {e}`")
                os.remove(os.getcwd() + "/userbot/modules/" + dosya)
                continue
            bot.send_message(PLUGIN_CHANNEL_ID, f"`Plugin Yüklendi\n\Dosya: {dosya}`")
        bot.send_message(PLUGIN_CHANNEL_ID, f"`Pluginler Yüklendi`")
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
