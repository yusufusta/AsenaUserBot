# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" İnsanlarla eğlenmek için yapılmış olan UserBot modülü. """

from asyncio import sleep
from random import choice, getrandbits, randint
from re import sub
import time
import asyncio

from collections import deque

import requests

from cowpy import cow

from userbot import CMD_HELP, ZALG_LIST
from userbot.events import register
from userbot.modules.admin import get_user_from_event

# ================= CONSTANT =================
EMOJIS = [
    "😂",
    "😂",
    "👌",
    "✌",
    "💞",
    "👍",
    "👌",
    "💯",
    "🎶",
    "👀",
    "😂",
    "👓",
    "👏",
    "👐",
    "🍕",
    "💥",
    "🍴",
    "💦",
    "💦",
    "🍑",
    "🍆",
    "😩",
    "😏",
    "👉👌",
    "👀",
    "👅",
    "😩",
    "🚰",
]

UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]

FACEREACTS = [
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    r"¯\_(ツ)_/¯",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
]

RUNS_STR = [
    "Hey! Nereye gidiyorsun?",
    "Ha? Ne? kaçtılar mı?",
    "ZZzzZZzz... Noldu? oh, yine onlarmış, boşver.",
    "Geri gel!",
    "Kaçın OneBot geliyor !!",
    "Duvara dikkat et!",
    "Beni onlarla sakın yalnız bırakma!!",
    "Kaçarsan, ölürsün.",
    "Şakacı seni, Ben heryerdeyim.",
    "Bunu yaptığına pişman olacaksın...",
    "/kickme tuşunuda deneyebilirsin, Eğlenceli olduğunu söylüyorlar.",
    "Git başka birini rahatsız et, burda kimse takmıyor.",
    "Kaçabilirsin ama saklanamazsın.",
    "Yapabildiklerin bunlar mı?",
    "Arkandayım...",
    "Misafirlerin var!",
    "Bunu kolay yoldan yapabiliriz, yada zor yoldan.",
    "Anlamıyorsun, değil mi?",
    "Haha, kaçsan iyi edersin.!",
    "Lütfen, hatırlat bana ne kadar aldırıyorum?",
    "Senin yerinde olsam daha hızlı kaçardım.",
    "Bu kesinlikle aradığımız robot.",
    "Belki şans sana güler.",
    "Ünlü son sözler.",
    "Ve sonsuza dek yok oldular, hiç görünmediler.",
    "\"Hey, bana bakın! Bottan kaçabiliyorum çok havalıyım!\" - bu kişi",
    "Evet evet, /kickme tuşuna şimdiden bas.",
    "İşte, bu yüzüğü alın ve Mordor'a gidin.",
    "Efsaneye göre onlar hala çalışıyor...",
    "Harry Potter'ın aksine, ebeveynlerin seni benden koruyamaz.",
    "Korku öfkeye, öfke nefrete, nefret acıya yol açar. Korku içinde kaçmaya devam edersen,"
    "bir sonraki Vader sen olabilirsin.",
    "Birden fazla hesaplama yapıldıktan sonra, dalaverelerine olan ilgimin tam olarak 0 olduğuna karar verdim.",
    "Efsaneye göre onlar hala çalışıyor.",
    "Devam et, seni burda istediğimize emin değilim.",
    "Sen bir sihirb- Oh. Bekle. Sen Harry değilsin, devam et.",
    "KORİDORDA KOŞMAYIN!",
    "Görüşürüz bebeğim.",
    "Kim köpekleri saldı?",
    "Komik çünkü kimse takmıyor.",
    "Ah, ne büyük kayıp. Bu seferkini sevmiştim.",
    "Açıkcası canım, umrumda değil.",
    "Sütüm tüm erkekleri avluya çekiyor... Daha hızlı koş!",
    "Gerçeği KALDIRAMAZSIN!",
    "Uzun zaman önce, çok çok uzaktaki bir galakside birileri takabilirdi. Ama artık değil.",
    "Hey, onlara bak! Kaçınılmaz banhammer'dan kaçıyorlar... Ne kadarda tatlı.",
    "Han önce vuruldu. Ben de öyle yapacağım",
    "Beyaz tavşanın, arkasında ne yapıyorsun?",
    "Doktorunda söyleyeceği gibi... KAÇ!",
]

HELLOSTR = [
    "Merhaba!",
    "‘Naber Müdür!",
    "Nasılsın’?",
    "‘Hey N'oluyor?",
    "Selam, selam, selam!",
    "Merhaba, kim var orada?, Ben konuşuyorum.",
    "Bunun kim oldugunu biliyorsun",
    "Hey Yo!",
    "N'aber.",
    "Selamlar ve selamlar!",
    "Merhaba, günışığı!",
    "Hey, n'aber, merhaba!",
    "Nasıl gidiyor’, küçük civciv?",
    "Ce-e!",
    "Naber-doody!",
    "Selam, birinci sınıf veledi!",
    "Barışalım!",
    "Selam, dostum!",
    "M-merhaba!",
]

SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

CRI = [
    "أ‿أ",
    "╥﹏╥",
    "(;﹏;)",
    "(ToT)",
    "(┳Д┳)",
    "(ಥ﹏ಥ)",
    "（；へ：）",
    "(T＿T)",
    "（πーπ）",
    "(Ｔ▽Ｔ)",
    "(⋟﹏⋞)",
    "（ｉДｉ）",
    "(´Д⊂ヽ",
    "(;Д;)",
    "（>﹏<）",
    "(TдT)",
    "(つ﹏⊂)",
    "༼☯﹏☯༽",
    "(ノ﹏ヽ)",
    "(ノAヽ)",
    "(╥_╥)",
    "(T⌓T)",
    "(༎ຶ⌑༎ຶ)",
    "(☍﹏⁰)｡",
    "(ಥ_ʖಥ)",
    "(つд⊂)",
    "(≖͞_≖̥)",
    "(இ﹏இ`｡)",
    "༼ಢ_ಢ༽",
    "༼ ༎ຶ ෴ ༎ຶ༽",
]

SLAP_TEMPLATES = [
    "{victim} kullanıcısını {item} ile {hits} .",
    "{victim} kullanıcısını {item} ile yüzüne {hits} .",
    "{victim} kullanıcısını {item} ile biraz {hits} .",
    "{victim} kullanıcısına {item} {throws} .",
    "{victim} kullanıcısını {item} ile yüzüne {throws} .",
    "{victim} kullanıcısına doğru {item} fırlatıyor.",
    "{victim} aptalına {item} ile tokat atıyor.",
    "{victim} kullanıcısını yere sabitleyıp ardı ardına {item} ile {hits} .",
    "{item} alarak {victim} {hits}.",
    "{victim} kullanıcısını sandalyeye bağlayıp {item} {throws} .",
    "{victim} kullanıcısını arkadaşca ittirerek lavda yüzmeyi öğrenmesini sağlıyor."
]

ITEMS = [
    "demir tencere",
    "büyük alabalık",
    "beyzbol sopası",
    "kriket sopası",
    "tahta baston",
    "çivi",
    "yazıcı",
    "kürek",
    "tüplü monitör",
    "fizik defteri",
    "tost makinası",
    "Richard Stallman'ın portresi",
    "televizyon",
    "beş ton kamyon",
    "koli bandı",
    "kitap",
    "dizüstü bilgisayar",
    "eski televizyon",
    "kayalı çuval",
    "gökkuşağı alabalığı",
    "plastik tavuk",
    "çivili sopa",
    "yangın söndürücü",
    "ağır taş",
    "kir yığını",
    "arı kovanı",
    "çürük et parçası",
    "ayı",
    "tonlarca tuğla",
]

THROW = [
    "atıyor",
    "fırlatıyor",
    "savuruyor",
    "yağdırıyor",
]

HIT = [
    "vuruyor",
    "sert vuruyor",
    "tokatlıyor",
    "yumrukluyor",
    "geçiriyor",
]

# ===========================================
@register(outgoing=True, pattern="^.karar$")
async def karar(e):
    msaj = ""
    if e.reply_to_msg_id:
        rep = await e.get_reply_message()
        replyto = rep.id
        msaj += f"[Dostum](tg://user?id={rep.from_id}), "
    else:
        e.edit("`Lütfen bir mesaja yanıt verin`")
        return
    yesno = requests.get('https://yesno.wtf/api').json()
    if yesno["answer"] == "yes":
        cevap = "evet"
    else:
        cevap = "hayır"
    msaj += f"Sanırım buna {cevap} diyeceğim."

    await e.delete()
    await e.client.send_message(
        e.chat_id,
        msaj,
        reply_to=replyto,
        file=yesno["image"]
    )

@register(outgoing=True, pattern=r"^.(\w+)say (.*)")
async def univsaye(cowmsg):
    """ .cowsay komutu bir şeyler söyleyen inek yapar """
    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)

    if arg == "cow":
        arg = "default"
    if arg not in cow.COWACTERS:
        return
    cheese = cow.get_cow(arg)
    cheese = cheese()

    await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")


@register(outgoing=True, pattern="^:/$", ignore_unsafe=True)
async def kek(keks):
    """ Kendinizi kontrol edin ;)"""
    uio = ["/", "\\"]
    for i in range(1, 15):
        time.sleep(0.3)
        await keks.edit(":" + uio[i % 2])


@register(pattern="^.slap(?: |$)(.*)", outgoing=True)
async def who(event):
    """ Hedeflenen kullanıcıya tokat atar. """
    replied_user = await get_user_from_event(event)
    if replied_user:
        replied_user = replied_user[0]
    else:
        return
    caption = await slap(replied_user, event)

    try:
        await event.edit(caption)

    except BaseException:
        await event.edit(
            "`Bu kişiyi tokatlayamam, yanıma sopa ve taş almam gerekecek !!`"
        )


async def slap(replied_user, event):
    """ Tokat atarken komik cümle kur !! """
    user_id = replied_user.id
    first_name = replied_user.first_name
    username = replied_user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = choice(SLAP_TEMPLATES)
    item = choice(ITEMS)
    hit = choice(HIT)
    throw = choice(THROW)

    caption = "Seden " + temp.format(
        victim=slapped, item=item, hits=hit, throws=throw)

    return caption


@register(outgoing=True, pattern="^-_-$", ignore_unsafe=True)
async def lol(lel):
    """ Tamam... """
    okay = "-_-"
    for i in range(10):
        okay = okay[:-1] + "_-"
        await lel.edit(okay)


@register(outgoing=True, pattern="^;_;$", ignore_unsafe=True)
async def fun(e):
    t = ";_;"
    for j in range(10):
        t = t[:-1] + "_;"
        await e.edit(t)


@register(outgoing=True, pattern="^.fp$")
async def facepalm(e):
    """ Utanmak  🤦‍♂ """
    await e.edit("🤦‍♂")


@register(outgoing=True, pattern="^.cry$")
async def cry(e):
    """ bunu yaparsan, her zaman ağlarım !! """
    await e.edit(choice(CRI))


@register(outgoing=True, pattern="^.cp(?: |$)(.*)")
async def copypasta(cp_e):
    """ copypasta """
    textx = await cp_e.get_reply_message()
    message = cp_e.pattern_match.group(1)

    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await cp_e.edit("`😂Bana💯BIR✌️mE🅱️In👐Ver👏`")
        return

    reply_text = choice(EMOJIS)
    b_char = choice(message).lower()
    for owo in message:
        if owo == " ":
            reply_text += choice(EMOJIS)
        elif owo in EMOJIS:
            reply_text += owo
            reply_text += choice(EMOJIS)
        elif owo.lower() == b_char:
            reply_text += "🅱️"
        else:
            if bool(getrandbits(1)):
                reply_text += owo.upper()
            else:
                reply_text += owo.lower()
    reply_text += choice(EMOJIS)
    await cp_e.edit(reply_text)


@register(outgoing=True, pattern="^.vapor(?: |$)(.*)")
async def vapor(vpr):
    """ Her şeyi vaporlaştırın! """
    reply_text = list()
    textx = await vpr.get_reply_message()
    message = vpr.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await vpr.edit("`Ｂａｎａ ｂｉｒ ｍｅｔｉｎ ｖｅｒ!`")
        return

    for charac in message:
        if 0x21 <= ord(charac) <= 0x7F:
            reply_text.append(chr(ord(charac) + 0xFEE0))
        elif ord(charac) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(charac)

    await vpr.edit("".join(reply_text))


@register(outgoing=True, pattern="^.str(?: |$)(.*)")
async def stretch(stret):
    """ Mesajı iyice uzatın."""
    textx = await stret.get_reply_message()
    message = stret.text
    message = stret.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await stret.edit("`Baaaaanaaaaa biiiiir meeeeetiiiiin veeeeer!`")
        return

    count = randint(3, 10)
    reply_text = sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count),
                     message)
    await stret.edit(reply_text)


@register(outgoing=True, pattern="^.zal(?: |$)(.*)")
async def zal(zgfy):
    """ Kaos duygusunu çağırın. """
    reply_text = list()
    textx = await zgfy.get_reply_message()
    message = zgfy.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await zgfy.edit(
            "`Ｂ̺ͬａ̠͑ｎ̵̉ａ̬͜ ｂ̶͔ｉ̼͚ｒ͈͞ ｍ̼͘ｅ̨̝ｔ͔͙ｉ̢ͮｎ̜͗ ｖ͢͜ｅ̗͐ｒ̴ͮ`"
        )
        return

    for charac in message:
        if not charac.isalpha():
            reply_text.append(charac)
            continue

        for _ in range(0, 3):
            charac += choice(ZALG_LIST[randint(0,2)]).strip()

        reply_text.append(charac)

    await zgfy.edit("".join(reply_text))
    

@register(outgoing=True, pattern="^.hi$")
async def hoi(hello):
    """ Herkesi selamlayın """
    await hello.edit(choice(HELLOSTR))


@register(outgoing=True, pattern="^.owo(?: |$)(.*)")
async def faces(owo):
    """ UwU """
    textx = await owo.get_reply_message()
    message = owo.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await owo.edit("` UwU bana bir metin ver! `")
        return

    reply_text = sub(r"(r|l)", "w", message)
    reply_text = sub(r"(R|L)", "W", reply_text)
    reply_text = sub(r"n([aeiou])", r"ny\1", reply_text)
    reply_text = sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
    reply_text = sub(r"\!+", " " + choice(UWUS), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += " " + choice(UWUS)
    await owo.edit(reply_text)


@register(outgoing=True, pattern="^.react$")
async def react_meme(react):
    """ UserBot'un her şeye tepki vermesini sağlayın. """
    await react.edit(choice(FACEREACTS))


@register(outgoing=True, pattern="^.shg$")
async def shrugger(shg):
    r""" ¯\_(ツ)_/¯ """
    await shg.edit(choice(SHGS))


@register(outgoing=True, pattern="^.run$")
async def runner_lol(run):
    await run.edit(choice(RUNS_STR))


@register(outgoing=True, pattern="^oof$")
async def oof(e):
    t = "oof"
    for j in range(16):
        t = t[:-1] + "of"
        await e.edit(t)

                      
@register(outgoing=True, pattern="^Oof$")
async def Oof(e):
    t = "Oof"
    for j in range(16):
        t = t[:-1] + "of"
        await e.edit(t)


@register(outgoing=True, pattern="^skrrt$")
async def oof(e):
    t = "skrrt"
    for j in range(16):
        t = t[:-1] + "rt"
        await e.edit(t)
        

@register(outgoing=True, pattern="^Skrrt$")
async def oof(e):
    t = "Skrrt"
    for j in range(16):
        t = t[:-1] + "rt"
        await e.edit(t)


@register(outgoing=True, pattern="^.fuk")
async def fuk(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0, 101)
    animation_chars = [
            "🍆       🍑️",
            "🍆     🍑️",
            "🍆  🍑️",
            "🍆🍑️💦"
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@register(outgoing=True, pattern="^.kalp (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    deq = deque(list("️❤️🧡💛💚💙💜🖤"))
    for _ in range(32):
        await asyncio.sleep(0.1)
        await event.edit("".join(deq))
        deq.rotate(1)
    await event.edit("❤️🧡💛" + input_str + "💚💙💜🖤")


@register(outgoing=True, pattern="^.10iq$")
async def iqless(e):
    await e.edit(
    "DÜÜÜT DÜÜÜTT AÇ YOLU AÇÇ HADİ ASLAN PARÇASI YOLU AÇ \n"
    "HADİ BAK ENGELLİ BEKLİYO BURDA HADİ DÜÜÜTTT ♿️ BAK \n"
    "SİNİRLENDİ ARKADAŞ HADİ YOLU AÇ HADİİ DÜÜÜT DÜÜTT BİİİPP \n"
    "HADİ BE HIZLI OLL DÜÜÜTT BİİİPPP ♿️♿️ BAK HIZLANDI ENGELLİ \n"
    "KARDEŞİMİZ SERİ KÖZ GETİR SERİ DÜÜÜTT DÜÜÜT DÜÜÜÜTTTTT \n"
    "BİİİİPPP BİİİİİPPP DÜÜÜTTT ♿️♿️♿️♿️ BAK ARTIYO SAYILARI \n"
    "AÇTIN MI YOLU AÇMADIN PÜÜÜÜ REZİİİLL DÜÜÜÜTTT ♿️♿️♿️ \n"
    "♿️♿️♿️ BAK KALABALIKLASTI BAK DELI GELIYOR DELIRDI DELI \n"
    "AC YOLU DUTDUTDURURURUDUTTT♿️♿️♿️♿️♿️♿️♿️♿️♿️ \n"
    "♿️♿️♿️♿️♿️KAFAYI YEDI BUNLAR AC LAAAAN YOLU"
    )
    
    
@register(outgoing=True, pattern="^.mizah$")
async def mizahshow(e):
    await e.edit(
    "⚠️⚠️⚠️MmMmMmMizahh Şoww😨😨😨😨😱😱😱😱😱 \n"
    "😱😱⚠️⚠️ 😂😂😂😂😂😂😂😂😂😂😂😂😂😂😱😵 \n"
    "😂😂👍👍👍👍👍👍👍👍👍👍👍👍👍 MiZah \n"
    "ŞeLaLesNdEn b1r yUdm aLdım✔️✔️✔️✔️ \n"
    "AHAHAHAHAHAHHAHAHAHAHAHAHAHAHAHAHAHHAHAHAHAHA \n"
    "HAHAHAHAHAHAHHAHAHAHAHAHAHA😂😂😂😂😂😂😂😂 \n"
    "😂 KOMİK LAN KOMİİİK \n"
    "heLaL LaN ✔️✔️✔️✔️✔️✔️✔️✔️👏👏👏👏👏👏👏👏 \n"
    "👏 EfSaNe mMmMiZah şooooovv 👏👏👏👏👏😂😂😂😂 \n"
    "😂😂😂😂😂😂⚠️ \n"
    "💯💯💯💯💯💯💯💯💯 \n"
    "KNK AYNI BİİİZ 😂😂😂👏👏 \n"
    "💯💯⚠️⚠️♿️AÇ YOLU POST SAHİBİ VE ONU ♿️SAVUNANLAR \n"
    "GELIYOR ♿️♿️ DÜÜTT♿️ \n"
    "DÜÜÜÜT♿️DÜÜT♿️💯💯⚠️ \n"
    "♿️KOMİİİK ♿️ \n"
    "CJWJCJWJXJJWDJJQUXJAJXJAJXJWJFJWJXJAJXJWJXJWJFIWIXJQJJQJASJAXJ \n"
    "AJXJAJXJJAJXJWJFWJJFWIIFIWICIWIFIWICJAXJWJFJEICIIEICIEIFIWICJSXJJS \n"
    "CJEIVIAJXBWJCJIQICIWJX💯💯💯💯💯💯😂😂😂😂😂😂😂 \n"
    "😂⚠️😂😂😂😂😂😂⚠️⚠️⚠️😂😂😂😂♿️♿️♿️😅😅 \n"
    "😅😂👏💯⚠️👏♿️🚨"
    )    


@register(outgoing=True, pattern="^.moon$")
async def moon(event):
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    try:
        for x in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.clock$")
async def clock(event):
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    try:
        for x in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.mock(?: |$)(.*)")
async def spongemocktext(mock):
    """ Yap ve gerçek eğlenceyi bul. """
    reply_text = list()
    textx = await mock.get_reply_message()
    message = mock.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await mock.edit("`bANa bIr mETin vEr!`")
        return

    for charac in message:
        if charac.isalpha() and randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)

    await mock.edit("".join(reply_text))


@register(outgoing=True, pattern="^.clap(?: |$)(.*)")
async def claptext(memereview):
    """ İnsanları övün! """
    textx = await memereview.get_reply_message()
    message = memereview.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await memereview.edit("`Hah, anlamı olmadan alkışlamıyorum!`")
        return
    reply_text = "👏 "
    reply_text += message.replace(" ", " 👏 ")
    reply_text += " 👏"
    await memereview.edit(reply_text)


@register(outgoing=True, pattern=r"^.f (.*)")
async def payf(event):
    paytext = event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8, paytext * 8, paytext * 2, paytext * 2, paytext * 2,
        paytext * 6, paytext * 6, paytext * 2, paytext * 2, paytext * 2,
        paytext * 2, paytext * 2)
    await event.edit(pay)


@register(outgoing=True, pattern="^.lfy (.*)")
async def let_me_google_that_for_you(lmgtfy_q):
    textx = await lmgtfy_q.get_reply_message()
    qry = lmgtfy_q.pattern_match.group(1)
    if qry:
        query = str(qry)
    elif textx:
        query = textx
        query = query.message
    query_encoded = query.replace(" ", "+")
    lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
    payload = {'format': 'json', 'url': lfy_url}
    r = requests.get('http://is.gd/create.php', params=payload)
    await lmgtfy_q.edit(f"İşte, keyfine bak.\
    \n[{query}]({r.json()['shorturl']})")


@register(pattern=r".scam(?: |$)(.*)", outgoing=True)
async def scam(event):
    """ Sahte sohbet eylemleri için küçük bir komut !! """
    options = [
        'typing', 'contact', 'game', 'location', 'voice', 'round', 'video',
        'photo', 'document', 'cancel'
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) is 0:
        scam_action = choice(options)
        scam_time = randint(30, 60)
    elif len(args) is 1:
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(30, 60)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) is 2:
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await event.edit("`Invalid Syntax !!`")
        return
    try:
        if (scam_time > 0):
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await sleep(scam_time)
    except BaseException:
        return


@register(pattern=r".type(?: |$)(.*)", outgoing=True)
async def typewriter(typew):
    """ Klavyenizi daktilo haline getirmek için küçük bir komut! """
    textx = await typew.get_reply_message()
    message = typew.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await typew.edit("`Bana bir metin ver!`")
        return
    sleep_time = 0.03
    typing_symbol = "|"
    old_text = ""
    await typew.edit(typing_symbol)
    await sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await sleep(sleep_time)
        await typew.edit(old_text)
        await sleep(sleep_time)


CMD_HELP.update({
    "memes":
    ".cowsay\
\nKullanım: bir şeyler söyleyen inek.\
\n\n:/\
\nKullanım: Kendinizi kontrol edin ;)\
\n\n.karar\
\nKullanım: Karar verin.\
\n\n-_-\
\nKullanım: Tamam...\
\n\n;_;\
\nKullanım: `-_-` gibi ama ağlıyor.\
\n\n.cp\
\nKullanım: Meşhur copypasta modülü\
\n\n.vapor\
\nKullanım: Her şeyi vaporlaştırın!\
\n\n.str\
\nKullanım: Mesajı iyice uzatın.\
\n\n.10iq\
\nKullanım: Aptallık seviyenizi ölçün !!\
\n\n.mizah\
\nKullanım: Aptallık seviyenizi ölçün !!\
\n\n.zal\
\nKullanım: Kaos duygusunu çağırın.\
\n\noof\
\nKullanım: ooooof\
\n\nskrrt\
\nKullanım: skrrrrt\
\n\n.fuk\
\nKullanım: ¯\_(ツ)_/¯\
\n\n.kalp\
\nKullanım: Sevginizi gösterin.\
\n\n.fp\
\nKullanım: Utanmak  🤦‍♂\
\n\n.moon\
\nKullanım: Ay animasyonu.\
\n\n.clock\
\nKullanım: Saat animasyonu.\
\n\n.hi\
\nKullanım: Herkesi selamlayın!\
\n\n.owo\
\nKullanım: UwU\
\n\n.react\
\nKullanım: UserBot'un her şeye tepki vermesini sağlayın.\
\n\n.slap\
\nKullanım: rastgele nesnelerle tokatlamak için mesaja cevap verin !!\
\n\n.cry\
\nKullanım: bunu yaparsan, her zaman ağlarım.\
\n\n.shg\
\nKullanım: ¯\_(ツ)_/¯\
\n\n.run\
\nKullanım: UserBot'un koşmasını sağlar!\
\n\n.mock\
\nKullanım: Yap ve gerçek eğlenceyi bul.\
\n\n.clap\
\nKullanım: İnsanları övün!\
\n\n.f <emoji/karakter>\
\nKullanım: Saygılar..\
\n\n.type\
\nKullanım: Klavyenizi daktilo haline getirmek için küçük bir komut!\
\n\n.lfy <sorgu>\
\nKullanım: Bırakın Google bunu sizin için araştırsın.\
\n\n.scam <eylem> <süre>\
\n[Mevcut eylemler: (typing, contact, game, location, voice, round, video, photo, document, cancel)]\
\nKullanım: Create fake chat actions, for fun. (Varsayılan eylem: typing)\
\n\n\nBunlardan bazıları için teşekkürler 🅱️ottom🅱️ext🅱️ot (@NotAMemeBot).\
\n\nUyarlamalar için teşekkürler @NaytSeyd"
})
