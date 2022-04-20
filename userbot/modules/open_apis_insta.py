import aiohttp
import requests
import asyncio
import json
import os
from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp
# from userbot.language import get_value


@register(outgoing=True, pattern="^.insta ?(.*)")
async def apis(event):
    degerler = event.pattern_match.group(1)

    model = ""
    url = ""
    username = ""

    try:
        txt = degerler.split()
        model = txt[0]
        if model == "stalk":
            username = txt[1]
        else:
            url = txt[1]
    except IndexError:
        return await event.edit("**Lütfen Kullanım Talimatını Okuyun!** >> `.asena insta`")

    if model == "post" or model == "igtv":
        await event.edit("__Medya Aranıyor..__")
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('https://open-apis-rest.up.railway.app/api/instapost?url=' + url) as response:

                html = await response.text()
                html2 = json.loads(html)

                if html2["status"] == "OK":
                    post1 = html2["data"]["post1"]["url"]

                    try:
                        post2 = html2["data"]["post2"]["url"]
                    except KeyError:
                        post2 = " "
                    try:
                        post3 = html2["data"]["post3"]["url"]
                    except KeyError:
                        post3 = " "
                    try:
                        post4 = html2["data"]["post4"]["url"]
                    except KeyError:
                        post4 = " "
                    try:
                        post5 = html2["data"]["post5"]["url"]
                    except KeyError:
                        post5 = " "
                    try:
                        post6 = html2["data"]["post6"]["url"]
                    except KeyError:
                        post6 = " "
                    try:
                        post7 = html2["data"]["post7"]["url"]
                    except KeyError:
                        post7 = " "
                    try:
                        post8 = html2["data"]["post8"]["url"]
                    except KeyError:
                        post8 = " "
                    try:
                        post9 = html2["data"]["post9"]["url"]
                    except KeyError:
                        post9 = " "
                    try:
                        post10 = html2["data"]["post10"]["url"]
                    except KeyError:
                        post10 = " "

                    if post10 == " ":
                        if post9 == " ":
                            if post8 == " ":
                                if post7 == " ":
                                    if post6 == " ":
                                        if post5 == " ":
                                            if post4 == " ":
                                                if post3 == " ":
                                                    if post2 == " ":
                                                        if html2["data"]["post1"]["type"] == "jpg" or html2["data"]["post1"]["type"] == "png":
                                                            await downloader(post1, "./insta1.jpg")
                                                            await event.client.send_file(event.chat_id, './insta1.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                            await delFile("./insta1.jpg")

                                                        else:
                                                            await downloader(post1, "./insta1.mp4")
                                                            await event.client.send_file(event.chat_id, './insta1.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                            await delFile("./insta1.mp4")

                                                    else:
                                                        if html2["data"]["post1"]["type"] == "jpg" or html2["data"]["post2"]["type"] == "png":
                                                            await downloader(post1, "./insta1.jpg")
                                                            await event.client.send_file(event.chat_id, './insta1.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                            await delFile("./insta1.jpg")

                                                        else:
                                                            await downloader(post1, "./insta1.mp4")
                                                            await event.client.send_file(event.chat_id, './insta1.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                            await delFile("./insta1.mp4")

                                                        if html2["data"]["post2"]["type"] == "jpg" or html2["data"]["post2"]["type"] == "png":
                                                            await downloader(post2, "./insta2.jpg")
                                                            await event.client.send_file(event.chat_id, './insta2.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                            await delFile("./insta2.jpg")

                                                        else:
                                                            await downloader(post2, "./insta2.mp4")
                                                            await event.client.send_file(event.chat_id, './insta2.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                            await delFile("./insta2.mp4")

                                                else:
                                                    if html2["data"]["post1"]["type"] == "jpg" or html2["data"]["post1"]["type"] == "png":
                                                        # os.system("wget -O {0} {1}".format("./insta1.jpeg", post1))
                                                        await downloader(post1, "./insta1.jpeg")
                                                        await event.client.send_file(event.chat_id, './insta1.jpeg', caption="@AsenaUserBot ile Yüklendi.")
                                                        await delFile("./insta1.jpeg")

                                                    else:
                                                        await downloader(post2, "./insta1.mp4")
                                                        await event.client.send_file(event.chat_id, './insta1.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                        await delFile("./insta1.mp4")

                                                    if html2["data"]["post2"]["type"] == "jpg" or html2["data"]["post2"]["type"] == "png":
                                                        # os.system("wget -O {0} {1}".format("./insta2.jpeg", post2))
                                                        await downloader(post2, "./insta2.jpeg")
                                                        await event.client.send_file(event.chat_id, './insta2.jpeg', caption="@AsenaUserBot ile Yüklendi.")
                                                        await delFile("./insta2.jpeg")

                                                    else:
                                                        await downloader(post2, "./insta2.mp4")
                                                        await event.client.send_file(event.chat_id, './insta2.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                        await delFile("./insta2.mp4")

                                                    if html2["data"]["post3"]["type"] == "jpg" or html2["data"]["post3"]["type"] == "png":
                                                        # os.system("wget -O {0} {1}".format("./insta3.jpeg", post3))
                                                        await downloader(post3, "./insta3.jpeg")
                                                        await event.client.send_file(event.chat_id, './insta3.jpeg', caption="@AsenaUserBot ile Yüklendi.")
                                                        await delFile("./insta3.jpeg")

                                                    else:
                                                        await downloader(post3, "./insta3.mp4")
                                                        await event.client.send_file(event.chat_id, './insta3.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                        await delFile("./insta3.mp4")
                                            else:
                                                if html2["data"]["post1"]["type"] == "jpg" or html2["data"]["post1"]["type"] == "png":
                                                    await downloader(post1, "./insta1.jpg")
                                                    await event.client.send_file(event.chat_id, './insta1.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                    await delFile("./insta1.jpg")

                                                else:
                                                    await downloader(post2, "./insta1.mp4")
                                                    await event.client.send_file(event.chat_id, './insta1.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                    await delFile("./insta1.mp4")

                                                if html2["data"]["post2"]["type"] == "jpg" or html2["data"]["post2"]["type"] == "png":
                                                    await downloader(post2, "./insta2.jpg")
                                                    await event.client.send_file(event.chat_id, './insta2.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                    await delFile("./insta2.jpg")

                                                else:
                                                    await downloader(post2, "./insta2.mp4")
                                                    await event.client.send_file(event.chat_id, './insta2.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                    await delFile("./insta2.mp4")

                                                if html2["data"]["post3"]["type"] == "jpg" or html2["data"]["post3"]["type"] == "png":
                                                    await downloader(post3, "./insta3.jpg")
                                                    await event.client.send_file(event.chat_id, './insta3.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                    await delFile("./insta3.jpg")

                                                else:
                                                    await downloader(post3, "./insta3.mp4")
                                                    await event.client.send_file(event.chat_id, './insta3.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                    await delFile("./insta3.mp4")

                                                if html2["data"]["post4"]["type"] == "jpg" or html2["data"]["post4"]["type"] == "png":
                                                    await downloader(post4, "./insta4.jpg")
                                                    await event.client.send_file(event.chat_id, './insta4.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                    await delFile("./insta4.jpg")

                                                else:
                                                    await downloader(post4, "./insta4.mp4")
                                                    await event.client.send_file(event.chat_id, './insta4.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                    await delFile("./insta4.mp4")
                                        else:
                                            if html2["data"]["post1"]["type"] == "jpg" or html2["data"]["post1"]["type"] == "png":
                                                await downloader(post1, "./insta1.jpg")
                                                await event.client.send_file(event.chat_id, './insta1.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                await delFile("./insta1.jpg")

                                            else:
                                                await downloader(post2, "./insta1.mp4")
                                                await event.client.send_file(event.chat_id, './insta1.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                await delFile("./insta1.mp4")

                                            if html2["data"]["post2"]["type"] == "jpg" or html2["data"]["post2"]["type"] == "png":
                                                await downloader(post2, "./insta2.jpg")
                                                await event.client.send_file(event.chat_id, './insta2.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                await delFile("./insta2.jpg")

                                            else:
                                                await downloader(post2, "./insta2.mp4")
                                                await event.client.send_file(event.chat_id, './insta2.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                await delFile("./insta2.mp4")

                                            if html2["data"]["post3"]["type"] == "jpg" or html2["data"]["post3"]["type"] == "png":
                                                await downloader(post3, "./insta3.jpg")
                                                await event.client.send_file(event.chat_id, './insta3.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                await delFile("./insta3.jpg")

                                            else:
                                                await downloader(post3, "./insta3.mp4")
                                                await event.client.send_file(event.chat_id, './insta3.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                await delFile("./insta3.mp4")

                                            if html2["data"]["post4"]["type"] == "jpg" or html2["data"]["post4"]["type"] == "png":
                                                await downloader(post4, "./insta4.jpg")
                                                await event.client.send_file(event.chat_id, './insta4.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                await delFile("./insta4.jpg")

                                            else:
                                                await downloader(post4, "./insta4.mp4")
                                                await event.client.send_file(event.chat_id, './insta4.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                await delFile("./insta4.mp4")

                                            if html2["data"]["post5"]["type"] == "jpg" or html2["data"]["post5"]["type"] == "png":
                                                await downloader(post5, "./insta5.jpg")
                                                await event.client.send_file(event.chat_id, './insta5.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                                await delFile("./insta5.jpg")

                                            else:
                                                await downloader(post5, "./insta5.mp4")
                                                await event.client.send_file(event.chat_id, './insta5.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                                await delFile("./insta5.mp4")
                                    else:
                                        if html2["data"]["post1"]["type"] == "jpg" or html2["data"]["post1"]["type"] == "png":
                                            await downloader(post1, "./insta1.jpg")
                                            await event.client.send_file(event.chat_id, './insta1.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta1.jpg")

                                        else:
                                            await downloader(post2, "./insta1.mp4")
                                            await event.client.send_file(event.chat_id, './insta1.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta1.mp4")

                                        if html2["data"]["post2"]["type"] == "jpg" or html2["data"]["post2"]["type"] == "png":
                                            await downloader(post2, "./insta2.jpg")
                                            await event.client.send_file(event.chat_id, './insta2.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta2.jpg")

                                        else:
                                            await downloader(post2, "./insta2.mp4")
                                            await event.client.send_file(event.chat_id, './insta2.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta2.mp4")

                                        if html2["data"]["post3"]["type"] == "jpg" or html2["data"]["post3"]["type"] == "png":
                                            await downloader(post3, "./insta3.jpg")
                                            await event.client.send_file(event.chat_id, './insta3.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta3.jpg")

                                        else:
                                            await downloader(post3, "./insta3.mp4")
                                            await event.client.send_file(event.chat_id, './insta3.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta3.mp4")

                                        if html2["data"]["post4"]["type"] == "jpg" or html2["data"]["post4"]["type"] == "png":
                                            await downloader(post4, "./insta4.jpg")
                                            await event.client.send_file(event.chat_id, './insta4.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta4.jpg")

                                        else:
                                            await downloader(post4, "./insta4.mp4")
                                            await event.client.send_file(event.chat_id, './insta4.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta4.mp4")

                                        if html2["data"]["post5"]["type"] == "jpg" or html2["data"]["post5"]["type"] == "png":
                                            await downloader(post5, "./insta5.jpg")
                                            await event.client.send_file(event.chat_id, './insta5.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta5.jpg")

                                        else:
                                            await downloader(post5, "./insta5.mp4")
                                            await event.client.send_file(event.chat_id, './insta5.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta5.mp4")

                                        if html2["data"]["post6"]["type"] == "jpg" or html2["data"]["post6"]["type"] == "png":
                                            await downloader(post6, "./insta6.jpg")
                                            await event.client.send_file(event.chat_id, './insta6.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta6.jpg")

                                        else:
                                            await downloader(post6, "./insta6.mp4")
                                            await event.client.send_file(event.chat_id, './insta6.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                            await delFile("./insta6.mp4")

                                else:
                                    if html2["data"]["post1"]["type"] == "jpg" or html2["data"]["post1"]["type"] == "png":
                                        await downloader(post1, "./insta1.jpg")
                                        await event.client.send_file(event.chat_id, './insta1.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta1.jpg")

                                    else:
                                        await downloader(post2, "./insta1.mp4")
                                        await event.client.send_file(event.chat_id, './insta1.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta1.mp4")

                                    if html2["data"]["post2"]["type"] == "jpg" or html2["data"]["post2"]["type"] == "png":
                                        await downloader(post2, "./insta2.jpg")
                                        await event.client.send_file(event.chat_id, './insta2.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta2.jpg")

                                    else:
                                        await downloader(post2, "./insta2.mp4")
                                        await event.client.send_file(event.chat_id, './insta2.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta2.mp4")

                                    if html2["data"]["post3"]["type"] == "jpg" or html2["data"]["post3"]["type"] == "png":
                                        await downloader(post3, "./insta3.jpg")
                                        await event.client.send_file(event.chat_id, './insta3.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta3.jpg")

                                    else:
                                        await downloader(post3, "./insta3.mp4")
                                        await event.client.send_file(event.chat_id, './insta3.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta3.mp4")

                                    if html2["data"]["post4"]["type"] == "jpg" or html2["data"]["post4"]["type"] == "png":
                                        await downloader(post4, "./insta4.jpg")
                                        await event.client.send_file(event.chat_id, './insta4.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta4.jpg")

                                    else:
                                        await downloader(post4, "./insta4.mp4")
                                        await event.client.send_file(event.chat_id, './insta4.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta4.mp4")

                                    if html2["data"]["post5"]["type"] == "jpg" or html2["data"]["post5"]["type"] == "png":
                                        await downloader(post5, "./insta5.jpg")
                                        await event.client.send_file(event.chat_id, './insta5.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta5.jpg")

                                    else:
                                        await downloader(post5, "./insta5.mp4")
                                        await event.client.send_file(event.chat_id, './insta5.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta5.mp4")

                                    if html2["data"]["post6"]["type"] == "jpg" or html2["data"]["post6"]["type"] == "png":
                                        await downloader(post6, "./insta6.jpg")
                                        await event.client.send_file(event.chat_id, './insta6.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta6.jpg")

                                    else:
                                        await downloader(post6, "./insta6.mp4")
                                        await event.client.send_file(event.chat_id, './insta6.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta6.mp4")

                                    if html2["data"]["post7"]["type"] == "jpg" or html2["data"]["post7"]["type"] == "png":
                                        await downloader(post7, "./insta7.jpg")
                                        await event.client.send_file(event.chat_id, './insta7.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta7.jpg")

                                    else:
                                        await downloader(post7, "./insta7.mp4")
                                        await event.client.send_file(event.chat_id, './insta7.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                        await delFile("./insta7.mp4")

                            else:
                                if html2["data"]["post1"]["type"] == "jpg" or html2["data"]["post1"]["type"] == "png":
                                    await downloader(post1, "./insta1.jpg")
                                    await event.client.send_file(event.chat_id, './insta1.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta1.jpg")

                                else:
                                    await downloader(post2, "./insta1.mp4")
                                    await event.client.send_file(event.chat_id, './insta1.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta1.mp4")

                                if html2["data"]["post2"]["type"] == "jpg" or html2["data"]["post2"]["type"] == "png":
                                    await downloader(post2, "./insta2.jpg")
                                    await event.client.send_file(event.chat_id, './insta2.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta2.jpg")

                                else:
                                    await downloader(post2, "./insta2.mp4")
                                    await event.client.send_file(event.chat_id, './insta2.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta2.mp4")

                                if html2["data"]["post3"]["type"] == "jpg" or html2["data"]["post3"]["type"] == "png":
                                    await downloader(post3, "./insta3.jpg")
                                    await event.client.send_file(event.chat_id, './insta3.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta3.jpg")

                                else:
                                    await downloader(post3, "./insta3.mp4")
                                    await event.client.send_file(event.chat_id, './insta3.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta3.mp4")

                                if html2["data"]["post4"]["type"] == "jpg" or html2["data"]["post4"]["type"] == "png":
                                    await downloader(post4, "./insta4.jpg")
                                    await event.client.send_file(event.chat_id, './insta4.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta4.jpg")

                                else:
                                    await downloader(post4, "./insta4.mp4")
                                    await event.client.send_file(event.chat_id, './insta4.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta4.mp4")

                                if html2["data"]["post5"]["type"] == "jpg" or html2["data"]["post5"]["type"] == "png":
                                    await downloader(post5, "./insta5.jpg")
                                    await event.client.send_file(event.chat_id, './insta5.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta5.jpg")

                                else:
                                    await downloader(post5, "./insta5.mp4")
                                    await event.client.send_file(event.chat_id, './insta5.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta5.mp4")

                                if html2["data"]["post6"]["type"] == "jpg" or html2["data"]["post6"]["type"] == "png":
                                    await downloader(post6, "./insta6.jpg")
                                    await event.client.send_file(event.chat_id, './insta6.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta6.jpg")

                                else:
                                    await downloader(post6, "./insta6.mp4")
                                    await event.client.send_file(event.chat_id, './insta6.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta6.mp4")

                                if html2["data"]["post7"]["type"] == "jpg" or html2["data"]["post7"]["type"] == "png":
                                    await downloader(post7, "./insta7.jpg")
                                    await event.client.send_file(event.chat_id, './insta7.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta7.jpg")

                                else:
                                    await downloader(post7, "./insta7.mp4")
                                    await event.client.send_file(event.chat_id, './insta7.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta7.mp4")

                                if html2["data"]["post8"]["type"] == "jpg" or html2["data"]["post8"]["type"] == "png":
                                    await downloader(post8, "./insta8.jpg")
                                    await event.client.send_file(event.chat_id, './insta8.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta8.jpg")

                                else:
                                    await downloader(post8, "./insta8.mp4")
                                    await event.client.send_file(event.chat_id, './insta8.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                    await delFile("./insta8.mp4")

                        else:
                            if html2["data"]["post1"]["type"] == "jpg" or html2["data"]["post1"]["type"] == "png":
                                await downloader(post1, "./insta1.jpg")
                                await event.client.send_file(event.chat_id, './insta1.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta1.jpg")

                            else:
                                await downloader(post2, "./insta1.mp4")
                                await event.client.send_file(event.chat_id, './insta1.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta1.mp4")

                            if html2["data"]["post2"]["type"] == "jpg" or html2["data"]["post2"]["type"] == "png":
                                await downloader(post2, "./insta2.jpg")
                                await event.client.send_file(event.chat_id, './insta2.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta2.jpg")

                            else:
                                await downloader(post2, "./insta2.mp4")
                                await event.client.send_file(event.chat_id, './insta2.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta2.mp4")

                            if html2["data"]["post3"]["type"] == "jpg" or html2["data"]["post3"]["type"] == "png":
                                await downloader(post3, "./insta3.jpg")
                                await event.client.send_file(event.chat_id, './insta3.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta3.jpg")

                            else:
                                await downloader(post3, "./insta3.mp4")
                                await event.client.send_file(event.chat_id, './insta3.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta3.mp4")

                            if html2["data"]["post4"]["type"] == "jpg" or html2["data"]["post4"]["type"] == "png":
                                await downloader(post4, "./insta4.jpg")
                                await event.client.send_file(event.chat_id, './insta4.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta4.jpg")

                            else:
                                await downloader(post4, "./insta4.mp4")
                                await event.client.send_file(event.chat_id, './insta4.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta4.mp4")

                            if html2["data"]["post5"]["type"] == "jpg" or html2["data"]["post5"]["type"] == "png":
                                await downloader(post5, "./insta5.jpg")
                                await event.client.send_file(event.chat_id, './insta5.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta5.jpg")

                            else:
                                await downloader(post5, "./insta5.mp4")
                                await event.client.send_file(event.chat_id, './insta5.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta5.mp4")

                            if html2["data"]["post6"]["type"] == "jpg" or html2["data"]["post6"]["type"] == "png":
                                await downloader(post6, "./insta6.jpg")
                                await event.client.send_file(event.chat_id, './insta6.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta6.jpg")

                            else:
                                await downloader(post6, "./insta6.mp4")
                                await event.client.send_file(event.chat_id, './insta6.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta6.mp4")

                            if html2["data"]["post7"]["type"] == "jpg" or html2["data"]["post7"]["type"] == "png":
                                await downloader(post7, "./insta7.jpg")
                                await event.client.send_file(event.chat_id, './insta7.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta7.jpg")

                            else:
                                await downloader(post7, "./insta7.mp4")
                                await event.client.send_file(event.chat_id, './insta7.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta7.mp4")

                            if html2["data"]["post8"]["type"] == "jpg" or html2["data"]["post8"]["type"] == "png":
                                await downloader(post8, "./insta8.jpg")
                                await event.client.send_file(event.chat_id, './insta8.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta8.jpg")

                            else:
                                await downloader(post8, "./insta8.mp4")
                                await event.client.send_file(event.chat_id, './insta8.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta8.mp4")

                            if html2["data"]["post9"]["type"] == "jpg" or html2["data"]["post9"]["type"] == "png":
                                await downloader(post9, "./insta9.jpg")
                                await event.client.send_file(event.chat_id, './insta9.jpg', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta9.jpg")

                            else:
                                await downloader(post9, "./insta9.mp4")
                                await event.client.send_file(event.chat_id, './insta9.mp4', caption="@AsenaUserBot ile Yüklendi.")
                                await delFile("./insta9.mp4")

                    else:
                        if html2["data"]["post1"]["type"] == "jpg" or html2["data"]["post1"]["type"] == "png":
                            await downloader(post1, "./insta1.jpg")
                            await event.client.send_file(event.chat_id, './insta1.jpg', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta1.jpg")

                        else:
                            await downloader(post2, "./insta1.mp4")
                            await event.client.send_file(event.chat_id, './insta1.mp4', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta1.mp4")

                        if html2["data"]["post2"]["type"] == "jpg" or html2["data"]["post2"]["type"] == "png":
                            await downloader(post2, "./insta2.jpg")
                            await event.client.send_file(event.chat_id, './insta2.jpg', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta2.jpg")

                        else:
                            await downloader(post2, "./insta2.mp4")
                            await event.client.send_file(event.chat_id, './insta2.mp4', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta2.mp4")

                        if html2["data"]["post3"]["type"] == "jpg" or html2["data"]["post3"]["type"] == "png":
                            await downloader(post3, "./insta3.jpg")
                            await event.client.send_file(event.chat_id, './insta3.jpg', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta3.jpg")

                        else:
                            await downloader(post3, "./insta3.mp4")
                            await event.client.send_file(event.chat_id, './insta3.mp4', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta3.mp4")

                        if html2["data"]["post4"]["type"] == "jpg" or html2["data"]["post4"]["type"] == "png":
                            await downloader(post4, "./insta4.jpg")
                            await event.client.send_file(event.chat_id, './insta4.jpg', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta4.jpg")

                        else:
                            await downloader(post4, "./insta4.mp4")
                            await event.client.send_file(event.chat_id, './insta4.mp4', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta4.mp4")

                        if html2["data"]["post5"]["type"] == "jpg" or html2["data"]["post5"]["type"] == "png":
                            await downloader(post5, "./insta5.jpg")
                            await event.client.send_file(event.chat_id, './insta5.jpg', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta5.jpg")

                        else:
                            await downloader(post5, "./insta5.mp4")
                            await event.client.send_file(event.chat_id, './insta5.mp4', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta5.mp4")

                        if html2["data"]["post6"]["type"] == "jpg" or html2["data"]["post6"]["type"] == "png":
                            await downloader(post6, "./insta6.jpg")
                            await event.client.send_file(event.chat_id, './insta6.jpg', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta6.jpg")

                        else:
                            await downloader(post6, "./insta6.mp4")
                            await event.client.send_file(event.chat_id, './insta6.mp4', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta6.mp4")

                        if html2["data"]["post7"]["type"] == "jpg" or html2["data"]["post7"]["type"] == "png":
                            await downloader(post7, "./insta7.jpg")
                            await event.client.send_file(event.chat_id, './insta7.jpg', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta7.jpg")

                        else:
                            await downloader(post7, "./insta7.mp4")
                            await event.client.send_file(event.chat_id, './insta7.mp4', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta7.mp4")

                        if html2["data"]["post8"]["type"] == "jpg" or html2["data"]["post8"]["type"] == "png":
                            await downloader(post8, "./insta8.jpg")
                            await event.client.send_file(event.chat_id, './insta8.jpg', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta8.jpg")

                        else:
                            await downloader(post8, "./insta8.mp4")
                            await event.client.send_file(event.chat_id, './insta8.mp4', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta8.mp4")

                        if html2["data"]["post9"]["type"] == "jpg" or html2["data"]["post9"]["type"] == "png":
                            await downloader(post9, "./insta9.jpg")
                            await event.client.send_file(event.chat_id, './insta9.jpg', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta9.jpg")

                        else:
                            await downloader(post9, "./insta9.mp4")
                            await event.client.send_file(event.chat_id, './insta9.mp4', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta9.mp4")

                        if html2["data"]["post10"]["type"] == "jpg" or html2["data"]["post10"]["type"] == "png":
                            await downloader(post10, "./insta10.jpg")
                            await event.client.send_file(event.chat_id, './insta10.jpg', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta10.jpg")

                        else:
                            await downloader(post10, "./insta10.mp4")
                            await event.client.send_file(event.chat_id, './insta10.mp4', caption="@AsenaUserBot ile Yüklendi.")
                            await delFile("./insta10.mp4")

                    await event.delete()

                else:
                    return await event.edit("Lütfen Bağlantınızı Kontrol Edin. Sorun hala devam ediyorsa destek ekibine ulaşın.")

    elif model == "reel":
        await event.edit("__Video Aranıyor..__")
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('https://open-apis-rest.up.railway.app/api/instareel?url=' + url) as response:

                html3 = await response.text()
                html4 = json.loads(html3)
                if html4["status"] == "OK":
                    await downloader(html4["data"]["url"], "./reel.mp4")
                    await event.client.send_file(event.chat_id, './reel.mp4', caption="@AsenaUserBot ile Yüklendi.")
                    await delFile("./reel.mp4")
                    await event.delete()
                else:
                    return await event.edit("Lütfen Bağlantınızı Kontrol Edin. Sorun hala devam ediyorsa destek ekibine ulaşın.")

    elif model == "stalk":
        await event.edit("__Profil Kontrol Ediliyor..__")
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('https://open-apis-rest.up.railway.app/api/instastalk?username=' + username) as response:

                html3 = await response.text()
                html4 = json.loads(html3)
                if html4["status"] == "OK":

                    stimg = html4["data"]["profile_pic"]
                    bio = html4["data"]["bio"]
                    postc = html4["data"]["post_count"]
                    follower = html4["data"]["followers"]
                    following = html4["data"]["following"]
                    ids = html4["data"]["id"]
                    popul = html4["data"]["popularity"]
                    avlike = html4["data"]["avarage_likes"]
                    avcm = html4["data"]["avarage_comments"]
                    avpt = html4["data"]["avarage_post_time"]
                    vperc = html4["data"]["video_percentage"]
                    pperc = html4["data"]["photo_percentage"]

                    if avlike == "n/a":
                        avlike = "Veri Yok"

                    # os.system("wget -O {0} {1}".format("./stalk.png", stimg))
                    await downloader(stimg, "./stalk.png")
                    await event.client.send_file(event.chat_id, './stalk.png', caption="**Kullanıcı Adı:** " + username + "\n**ID:** " + ids + "\n**Bio:** " + bio + "\n\n**Post Sayısı:** " + postc + "\n**Takipçiler:** " + follower + "\n**Takip Edilenler:** " + following + "\n**Popülerite:** " + popul + "\n**Ortalama Beğeni:** " + avlike + "\n**Ortalama Yorum:** " + avcm + "\n**Ortalama Post Paylaşımı:** " + avpt + "\n**Video Gönderi:** " + vperc + "\n**Fotoğraf Gönderi:** " + pperc)
                    delFile("./stalk.png")
                    await event.delete()
                else:
                    return await event.edit("Hesap gizli veya böyle bir hesap yok.")
    else:
        return await event.edit("**Lütfen Kullanım Talimatını Okuyun!** >> `.asena insta`")


async def downloader(media, name):
    resp = requests.get(media)
    with open(name, "wb") as f:
        f.write(resp.content)
    return True


async def delFile(file):
    os.remove(file)
    return True


Help = CmdHelp('insta')
Help.add_command('insta',
                 '<model> <url / username>',
                 'Çok amaçlı Instagram Aracı.',
                 'insta post https://www.instagram.com/p/CRYjfAPH1Jh/ \n' +
                 "insta reel https://www.instagram.com/reel/CaOGSyzA6qw \n" +
                 "insta igtv https://www.instagram.com/p/CIOeMERHXEt/ \n" +
                 "insta stalk lilmiquela \n"
                 )
Help.add_info("@phaticusthiccy tarafından yapılmıştır.")
Help.add()
