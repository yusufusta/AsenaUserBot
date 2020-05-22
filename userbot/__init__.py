# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Thanks github.com/spechide for creating inline bot support.
# Asena UserBot - Yusuf Usta
""" UserBot hazırlanışı. """

import os
import re

from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from math import ceil
import importlib

from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from dotenv import load_dotenv
from requests import get
from telethon.tl.types import InputMessagesFilterDocument
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient, custom, events
from telethon.sessions import StringSession
from telethon.utils import get_peer_id
load_dotenv("config.env")


def paginate_help(page_number, loaded_modules, prefix):
    number_of_rows = 5
    number_of_cols = 2
    helpable_modules = []
    for p in loaded_modules:
        if not p.startswith("_"):
            helpable_modules.append(p)
    helpable_modules = sorted(helpable_modules)
    modules = [custom.Button.inline(
        "{} {}".format("🔸", x),
        data="ub_modul_{}".format(x))
        for x in helpable_modules]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[modulo_page * number_of_rows:number_of_rows * (modulo_page + 1)] + \
            [
            (custom.Button.inline("⬅️Geri", data="{}_prev({})".format(prefix, modulo_page)),
             custom.Button.inline("İleri➡️", data="{}_next({})".format(prefix, modulo_page)))
        ]
    return pairs


# Bot günlükleri kurulumu:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

ASYNC_POOL = []

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.info("En az python 3.6 sürümüne sahip olmanız gerekir."
              "Birden fazla özellik buna bağlıdır. Bot kapatılıyor.")
    quit(1)

# Yapılandırmanın önceden kullanılan değişkeni kullanarak düzenlenip düzenlenmediğini kontrol edin.
# Temel olarak, yapılandırma dosyası için kontrol.
CONFIG_CHECK = os.environ.get(
    "___________LUTFEN_______BU_____SATIRI_____SILIN__________", None)

if CONFIG_CHECK:
    LOGS.info(
        "Lütfen ilk hashtag'de belirtilen satırı config.env dosyasından kaldırın"
    )
    quit(1)

# Telegram API KEY ve HASH
API_KEY = os.environ.get("API_KEY", None)
API_HASH = os.environ.get("API_HASH", None)

SILINEN_PLUGIN = {}
# UserBot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# Kanal / Grup ID yapılandırmasını günlüğe kaydetme.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", None))

# UserBot günlükleme özelliği.
BOTLOG = sb(os.environ.get("BOTLOG", "False"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

# Hey! Bu bir bot. Endişelenme ;)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

# Güncelleyici için Heroku hesap bilgileri.
HEROKU_MEMEZ = sb(os.environ.get("HEROKU_MEMEZ", "False"))
HEROKU_APPNAME = os.environ.get("HEROKU_APPNAME", None)
HEROKU_APIKEY = os.environ.get("HEROKU_APIKEY", None)

# Güncelleyici için özel (fork) repo linki.
UPSTREAM_REPO_URL = os.environ.get(
    "UPSTREAM_REPO_URL",
    "https://github.com/quiec/AsenaUserBot.git")

# Ayrıntılı konsol günlügü
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

# SQL Veritabanı
DB_URI = os.environ.get("DATABASE_URL", "sqlite://")

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)

# AUTO PP
AUTO_PP = os.environ.get("AUTO_PP", None)

# Chrome sürücüsü ve Google Chrome dosyaları
CHROME_DRIVER = os.environ.get("CHROME_DRIVER", None)
GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)

PLUGINID = os.environ.get("PLUGIN_CHANNEL_ID", None)
# Plugin İçin
if not PLUGINID:
    PLUGIN_CHANNEL_ID = "me"
else:
    PLUGIN_CHANNEL_ID = int(PLUGINID)

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)

# Lydia API
LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)

# Anti Spambot
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Youtube API key
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)

# Saat & Tarih - Ülke ve Saat Dilimi
COUNTRY = str(os.environ.get("COUNTRY", ""))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# Temiz Karşılama
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

# Last.fm Modülü
BIO_PREFIX = os.environ.get("BIO_PREFIX", None)
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)

LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    lastfm = LastFMNetwork(api_key=LASTFM_API,
                           api_secret=LASTFM_SECRET,
                           username=LASTFM_USERNAME,
                           password_hash=LASTFM_PASS)
else:
    lastfm = None

# Google Drive Modülü
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

# Inline bot çalışması için
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

# Genius modülünün çalışması için buradan değeri alın https://genius.com/developers her ikisi de aynı değerlere sahiptir
GENIUS = os.environ.get("GENIUS", None)
CMD_HELP = {}


# CloudMail.ru ve MEGA.nz ayarlama
if not os.path.exists('bin'):
    os.mkdir('bin')

binaries = {
    "https://raw.githubusercontent.com/yshalsager/megadown/master/megadown":
    "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py":
    "bin/cmrudl"
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

# 'bot' değişkeni
if STRING_SESSION:
    # pylint: devre dışı=geçersiz ad
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: devre dışı=geçersiz ad
    bot = TelegramClient("userbot", API_KEY, API_HASH)


if os.path.exists("learning-data-root.check"):
    os.remove("learning-data-root.check")
else:
    LOGS.info("Braincheck dosyası yok, getiriliyor...")

URL = 'https://raw.githubusercontent.com/quiec/databasescape/master/learning-data-root.check'

with open('learning-data-root.check', 'wb') as load:
    load.write(get(URL).content)


async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "Özel hata günlüğünün çalışması için yapılandırmadan BOTLOG_CHATID değişkenini ayarlamanız gerekir.")
        quit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "Günlüğe kaydetme özelliğinin çalışması için yapılandırmadan BOTLOG_CHATID değişkenini ayarlamanız gerekir.")
        quit(1)

    elif not BOTLOG or not LOGSPAMMER:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Hesabınızın BOTLOG_CHATID grubuna mesaj gönderme yetkisi yoktur. "
            "Grup ID'sini doğru yazıp yazmadığınızı kontrol edin.")
        quit(1)
if BOT_TOKEN != None:
    tgbot = TelegramClient(
        "TG_BOT_TOKEN",
        api_id=API_KEY,
        api_hash=API_HASH
    ).start(bot_token=BOT_TOKEN)
else:
    tgbot = None

with bot:
    try:
        bot(JoinChannelRequest("@AsenaUserBot"))
        bot(JoinChannelRequest("@AsenaSupport"))

        moduller = CMD_HELP
        me = bot.get_me()
        uid = me.id


        @tgbot.on(events.NewMessage(pattern='/start'))
        async def handler(event):
            if not event.message.from_id == uid:
                await event.reply(f'`Merhaba ben` @AsenaUserBot`! Ben sahibime (`@{me.username}`) yardımcı olmak için varım, yaani sana yardımcı olamam :/ Ama sen de bir Asena açabilirsin; Kanala bak` @AsenaUserBot')
            else:
                await event.reply(f'`Senin için çalışıyorum :) Seni seviyorum. ❤️`')

        @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query == "@AsenaUserBot":
                rev_text = query[::-1]
                buttons = paginate_help(0, moduller, "helpme")
                result = builder.article(
                    f"Lütfen Sadece .yardım Komutu İle Kullanın",
                    text="{}\nYüklenen Modül Sayısı: {}".format(
                        "Merhaba! Ben @AsenaUserBot kullanıyorum!\n\nhttps://github.com/quiec/AsenaUserBot", len(moduller)),
                    buttons=buttons,
                    link_preview=False
                )
            elif query.startswith("tb_btn"):
                result = builder.article(
                    "© @AsenaUserBot",
                    text=f"@AsenaUserBot ile güçlendirildi",
                    buttons=[],
                    link_preview=True
                )
            elif query.startswith("http"):
                parca = query.split(" ")
                result = builder.article(
                    "Dosya Yüklendi",
                    text=f"**Dosya başarılı bir şekilde {parca[2]} sitesine yüklendi!**\n\nYükleme zamanı: {parca[1][:3]} saniye\n[‏‏‎ ‎]({parca[0]})",
                    buttons=[
                        [custom.Button.url('URL', parca[0])]
                    ],
                    link_preview=True
                )
            else:
                result = builder.article(
                    "© @AsenaUserBot",
                    text="""@AsenaUserBot'u kullanmayı deneyin!
Hesabınızı bot'a çevirebilirsiniz ve bunları kullanabilirsiniz. Unutmayın, siz başkasının botunu yönetemezsiniz! Alttaki GitHub adresinden tüm kurulum detayları anlatılmıştır.""",
                    buttons=[
                        [custom.Button.url("Kanala Katıl", "https://t.me/AsenaUserBot"), custom.Button.url(
                            "Gruba Katıl", "https://t.me/AsenaSupport")],
                        [custom.Button.url(
                            "GitHub", "https://github.com/quiec/AsenaUserBot")]
                    ],
                    link_preview=False
                )
            await event.answer([result] if result else None)

        @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_next\((.+?)\)")
        ))
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number + 1, moduller, "helpme")
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Lütfen kendine bir @AsenaUserBot aç, benim mesajlarımı düzenlemeye çalışma!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_prev\((.+?)\)")
        ))
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number - 1,
                    moduller,  # pylint:disable=E0602
                    "helpme"
                )
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Lütfen kendine bir @AsenaUserBot aç, benim mesajlarımı düzenlemeye çalışma!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"ub_modul_(.*)")
        ))
        async def on_plug_in_callback_query_handlerm(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                modul_name = event.data_match.group(1).decode("UTF-8")

                cmdhel = str(CMD_HELP[modul_name])
                if len(cmdhel) > 90:
                    help_string = str(CMD_HELP[modul_name])[
                        :90] + "\n\nDevamı için .asena " + modul_name + " yazın."
                else:
                    help_string = str(CMD_HELP[modul_name])

                reply_pop_up_alert = help_string if help_string is not None else \
                    "{} modülü için herhangi bir döküman yazılmamış.".format(
                        modul_name)
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            else:
                reply_pop_up_alert = "Lütfen kendine bir @AsenaUserBot aç, benim mesajlarımı düzenlemeye çalışma!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
    except:
        LOGS.info(
            "Botunuzda inline desteği devre dışı bırakıldı. "
            "Etkinleştirmek için bir bot token tanımlayın ve botunuzda inline modunu etkinleştirin. "
            "Eğer bunun dışında bir sorun olduğunu düşünüyorsanız bize ulaşın."
        )

    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except:
        LOGS.info(
            "BOTLOG_CHATID ortam değişkeni geçerli bir varlık değildir. "
            "Ortam değişkenlerinizi / config.env dosyanızı kontrol edin."
        )
        quit(1)


# Küresel Değişkenler
COUNT_MSG = 0
USERS = {}
BRAIN_CHECKER = []
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
ISAFK = False
AFKREASON = None
ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
    [
    " ̍", " ̎", " ̄", " ̅", " ̿", " ̑", " ̆", " ̐", " ͒", " ͗",
    " ͑", " ̇", " ̈", " ̊", " ͂", " ̓", " ̈́", " ͊", " ͋", " ͌",
    " ̃", " ̂", " ̌", " ͐", " ́", " ̋", " ̏", " ̽", " ̉", " ͣ",
    " ͤ", " ͥ", " ͦ", " ͧ", " ͨ", " ͩ", " ͪ", " ͫ", " ͬ", " ͭ",
    " ͮ", " ͯ", " ̾", " ͛", " ͆", " ̚"
],
    [
    " ̕",
    " ̛",
    " ̀",
    " ́",
    " ͘",
    " ̡",
    " ̢",
    " ̧",
    " ̨",
    " ̴",
    " ̵",
    " ̶",
    " ͜",
    " ͝",
    " ͞",
    " ͟",
    " ͠",
    " ͢",
    " ̸",
    " ̷",
    " ͡",
]]
