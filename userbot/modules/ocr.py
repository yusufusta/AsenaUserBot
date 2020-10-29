# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


import os
from requests import post
from userbot import bot, OCR_SPACE_API_KEY, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("ocr")

# ████████████████████████████████ #

async def ocr_space_file(filename,
                         overlay=False,
                         api_key=OCR_SPACE_API_KEY,
                         language='tur'):
    """ OCR.space API yerel dosya ister.
        Python3.5 ve üzeri için - 2.7 üzerinde test edilmedi.
    :param filename: Dosya yolu ve adı.
    :param overlay: Cevabınızda OCR.space yerleşimi gerekli mi?
                    Varsayılan olarak Hayır.
    :param api_key: OCR.space API key.
                    varsayılan olarak 'merhabadünya'.
    :param language: OCR'de kullanılacak dil kodu.
                    Mevcut dil kodlarının listesi burudan bulunabilir https://ocr.space/OCRAPI
                    Varsayılan olarak 'tr'.
    :return: Sonuçlar JSON formatında gelir.
    """

    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    return r.json()


@register(pattern=r".ocr (.*)", outgoing=True)
async def ocr(event):
    await event.edit(LANG['READING'])
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await bot.download_media(
        await event.get_reply_message(), TEMP_DOWNLOAD_DIRECTORY)
    test_file = await ocr_space_file(filename=downloaded_file_name,
                                     language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException:
        await event.edit(LANG['CANT_READ'])
    else:
        await event.edit(f"`{LANG['READ']}`\n\n{ParsedText}"
                         )
    os.remove(downloaded_file_name)

CmdHelp('ocr').add_command(
    'ocr', '<dil>', 'Metin ayıklamak için bir resme veya çıkartmaya cevap verin.'
).add_info(
    'Dil kodlarını [buradan](https://ocr.space/ocrapi) alın.'
).add()