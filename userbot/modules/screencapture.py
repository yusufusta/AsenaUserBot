# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


import io
import traceback
from re import match
from selenium import webdriver
from asyncio import sleep
from selenium.webdriver.chrome.options import Options
from userbot.events import register
from userbot import GOOGLE_CHROME_BIN, CHROME_DRIVER, CMD_HELP


@register(pattern=r".ss (.*)", outgoing=True)
async def capture(url):
    """ .ss komutu, belirttiğin herhangi bir siteden ekran görüntüsü alır ve sohbete gönderir. """
    await url.edit("`İşleniyor...`")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--test-type")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER,
                              options=chrome_options)
    input_str = url.pattern_match.group(1)
    link_match = match(r'\bhttps?://.*\.\S+', input_str)
    if link_match:
        link = link_match.group()
    else:
        await url.edit("`Ekran görüntüsü alabilmem için geçerli bir bağlantı vermelisin.`")
        return
    driver.get(link)
    height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
    )
    width = driver.execute_script(
        "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
    )
    driver.set_window_size(width + 125, height + 125)
    wait_for = height / 1000
    await url.edit(f"`Sayfanın ekran görüntüsü oluşturuluyor...`\
    \n`Sayfanın yüksekliği: {height} piksel`\
    \n`Sayfanın genişliği: {width} piksel`\
    \n`Sayfanın yüklenmesi için {int(wait_for)} saniye beklendi.`")
    await sleep(int(wait_for))
    im_png = driver.get_screenshot_as_png()
    # Sayfanın ekran görüntüsü kaydedilir.
    driver.close()
    message_id = url.message.id
    if url.reply_to_msg_id:
        message_id = url.reply_to_msg_id
    with io.BytesIO(im_png) as out_file:
        out_file.name = "ekran_goruntusu.png"
        await url.edit("`Ekran görüntüsü karşıya yükleniyor...`")
        await url.client.send_file(url.chat_id,
                                   out_file,
                                   caption=input_str,
                                   force_document=True,
                                   reply_to=message_id)


CMD_HELP.update({
    "ss":
    ".ss <url>\
    \nKullanım: Belirtilen web sitesinden bir ekran görüntüsü alır ve gönderir.\
    \nGeçerli bir site bağlantısı örneği: `https://devotag.com`"
})
