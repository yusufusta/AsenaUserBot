#!/usr/bin/env python3
# (c) https://t.me/TelethonChat/37677
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html.

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("""Lütfen my.telegram.org adresine gidin
Telegram hesabınızı kullanarak giriş yapın
API Development Tools kısmına tıklayın
Gerekli ayrıntıları girerek yeni bir uygulama oluşturun""")
APP_ID = int(input("APP ID girin: "))
API_HASH = input("API HASH girin: ")

with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    print(client.session.save())
