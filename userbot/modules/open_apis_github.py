import aiohttp
import asyncio
import json
import requests
import os
from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp
# from userbot.language import get_value

def download(url):
    response = requests.get(url)
    file = open("./gh.png", "wb")
    file.write(response.content)
    file.close()
    return True

@register(outgoing=True, pattern="^.github ?(.*)")
async def apis(event):
    degerler = event.pattern_match.group(1)

    try:
        txt = degerler.split()
        us = txt[0]
    except IndexError:
        return await event.edit("**Eksik Paramatreler!**\n\n**Örnek:** `github phaticusthiccy`")

    await event.edit("__Bilgiler Toplanıyor..__")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get('https://open-apis-rest.up.railway.app/api/github?username=' + us) as response:

            html = await response.text()
            html2 = json.loads(html)
            if html2["status"] == "OK":

                username = html2["data"]["user"]["username"]
                name = html2["data"]["user"]["name"]
                gh_url = html2["data"]["user"]["github_url"]
                bio = html2["data"]["user"]["bio"]
                img = html2["data"]["user"]["avatar"]
                cr_date = html2["data"]["user"]["creation_date"]
                followers = html2["data"]["user"]["followers"]
                following = html2["data"]["user"]["following"]
                orgs = html2["data"]["user"]["organizations"]
                cont_rep = html2["data"]["user"]["contributed_repositories"]
                hireable = html2["data"]["user"]["hireable"]
                repos = html2["data"]["user"]["repositories"]
                stars = html2["data"]["user"]["stargazers"]
                starred = html2["data"]["user"]["starred_repositories"]
                sponsors = html2["data"]["user"]["sponsors"]
                sponsoring = html2["data"]["user"]["sponsoring"]
                forkers = html2["data"]["user"]["forkers"]
                watchers = html2["data"]["user"]["watchers"]
                watching = html2["data"]["user"]["watching_repositories"]

                commits = html2["data"]["activity"]["commits"]
                rev_prs = html2["data"]["activity"]["reviewed_pull_requests"]
                op_prs = html2["data"]["activity"]["opened_pull_requests"]
                op_iss = html2["data"]["activity"]["opened_issues"]
                iss_comm = html2["data"]["activity"]["issue_comments"]

                total_add = html2["data"]["repositories"]["total_added_lines"]
                total_rem = html2["data"]["repositories"]["total_removed_lines"]
                licenses = html2["data"]["repositories"]["preferred_license"]
                relases = html2["data"]["repositories"]["relases"]
                packages = html2["data"]["repositories"]["packages"]
                used_space = html2["data"]["repositories"]["used_space"]

                repo_lang = html2["data"]["languages"]["used_repo_languages"]
                all_lang = html2["data"]["languages"]["used_all_languages"]
                most_used = html2["data"]["languages"]["most_used_languages"][0]["language"]

                # ach1_name   = html2["data"]["achievements"][0]["achievement"]
                # ach1_capt   = html2["data"]["achievements"][0]["caption"]
                # ach1_class  = html2["data"]["achievements"][0]["class"]
                # ach2_name   = html2["data"]["achievements"][1]["achievement"]
                # ach2_capt   = html2["data"]["achievements"][1]["caption"]
                # ach2_class  = html2["data"]["achievements"][1]["class"]
                # ach3_name   = html2["data"]["achievements"][2]["achievement"]
                # ach3_capt   = html2["data"]["achievements"][2]["caption"]
                # ach3_class  = html2["data"]["achievements"][2]["class"]

                if "Not" in hireable:
                    hh = "Hayır"
                else:
                    hh = "Evet"

                sonuc = """
**Kullanıcı Adı:** {}
**İsim:** {}
**Bağlantı:** {}
**Bio:** {}
**Oluşturma Zamanı:** {}
**Takipçiler:** {}
**Takip Edilenler:** {}
**Organizasyonlar:** {}
**Katkıda Bulunan Projeler:** {}
**Kiralanabilir mi?:** {}
**Depo Sayısı:** {}
**Yıldız Sayısı:** {}
**Yıldızlanan Depo Sayısı:** {}
**Sponsorlar:** {}
**Sponsor Olunanlar:** {}
**Fork Sayısı:** {}
**İzleyenler:** {}
**İzlenenler:** {}

**Commit Sayısı:** {}
**Değerlendirilen PR Sayısı:** {}
**Açılan PR Sayısı:** {}
**Açılan Hata Bildirimleri:** {}
**Yapılan Yorumlar:** {}

**Eklenen Kod Satırı:** {}
**Silinen Kod Satırı:** {}
**Tercih Edilen Lisans:** {}
**Yayınlanan Sürümler:** {}
**Paket Sayısı:** {}
**Kullanılan Alan:** {}

**Toplam Depo Dili:** {}
**Toplam Kullanılan Dil:** {}
**En Çok Kullanılan Dil:** {}
                """.format(
                    username, name, gh_url, bio, cr_date, followers, following,
                    orgs, cont_rep, hh, repos, stars, starred, sponsors, sponsoring,
                    forkers, watchers, watching, commits, rev_prs, op_prs, op_iss,
                    iss_comm, total_add, total_rem, licenses, relases, packages, used_space,
                    repo_lang, all_lang, most_used
                )
                download(img)
                reply = await event.client.send_file(event.chat_id, './gh.png')
                os.remove("./gh.png")
                await event.client.send_message(event.chat_id, sonuc, reply_to=reply, link_preview=False)
                await event.delete()
            else:
                if "User" in html2["error"]:
                    return await event.edit("**" + degerler + "** Adında Herhangi Bir Kullanıcı Bulunamadı.")
                else:
                    return await event.edit("Sunucu Yoğun! Lütfen Daha Sonra Tekrar Deneyin.")

Help = CmdHelp('github')
Help.add_command('github',
                 '<kullanıcı adı>',
                 'Github Kullanıcısının Bilgilerini Gösterir.',
                 'github phaticusthiccy'
                 )
Help.add_info("@phaticusthiccy tarafından yapılmıştır.")
Help.add()
