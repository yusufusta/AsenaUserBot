# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


"""
Bu modül commit sayısına bağlı olarak botu günceller.
"""

from os import remove, execle, path, makedirs, getenv, environ
from shutil import rmtree
import asyncio
import sys

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HELP, bot, HEROKU_APIKEY, HEROKU_APPNAME, UPSTREAM_REPO_URL, HEROKU_MEMEZ
from userbot.events import register

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), 'requirements.txt')


async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            ' '.join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@register(outgoing=True, pattern=r"^\.update(?: |$)(.*)")
async def upstream(ups):
    ".update komutu ile botunun güncel olup olmadığını denetleyebilirsin."
    await ups.edit("`Güncellemeler denetleniyor...`")
    conf = ups.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_update = False

    try:
        txt = "`Güncelleme başarısız oldu!"
        txt += "Bazı sorunlarla karşılaştık.`\n\n**LOG:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await ups.edit(f'{txt}\n`{error} klasörü bulunamadı.`')
        repo.__del__()
        return
    except GitCommandError as error:
        await ups.edit(f'{txt}\n`Git hatası! {error}`')
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            await ups.edit(
                f"`{error} klasörü bir git reposu gibi görünmüyor.\
            \nFakat bu sorunu .update now komutuyla botu zorla güncelleyerek çözebilirsin.`"
            )
            return
        repo = Repo.init()
        origin = repo.create_remote('upstream', off_repo)
        origin.fetch()
        force_update = True
        repo.create_head('master', origin.refs.seden)
        repo.heads.seden.set_tracking_branch(origin.refs.sql)
        repo.heads.seden.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != 'master':
        await ups.edit(
            f'**[Güncelleyici]:**` Galiba Asena botunu modifiye ettin ve kendi branşını kullanıyorsun: ({ac_br}). '
            'Bu durum güncelleyicinin kafasını karıştırıyor,'
            'Güncelleme nereden çekilecek?'
            'Lütfen seden botunu resmi repodan kullan.`')
        repo.__del__()
        return

    try:
        repo.create_remote('upstream', off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if not changelog and not force_update:
        await ups.edit(
            f'\n`Botun` **tamamen güncel!** `Branch:` **{ac_br}**\n')
        repo.__del__()
        return

    if conf != "now" and not force_update:
        changelog_str = f'**{ac_br} için yeni güncelleme mevcut!\n\nDeğişiklikler:**\n`{changelog}`'
        if len(changelog_str) > 4096:
            await ups.edit("`Değişiklik listesi çok büyük, dosya olarak görüntülemelisin.`")
            file = open("degisiklikler.txt", "w+")
            file.write(changelog_str)
            file.close()
            await ups.client.send_file(
                ups.chat_id,
                "degisiklikler.txt",
                reply_to=ups.id,
            )
            remove("degisiklikler.txt")
        else:
            await ups.edit(changelog_str)
        await ups.respond('`Güncellemeyi yapmak için \".update now\" komutunu kullan.`')
        return

    if force_update:
        await ups.edit(
            '`Güncel stabil userbot kodu zorla eşitleniyor...`')
    else:
        await ups.edit('`Bot güncelleştiriliyor...`')
    # Bot bir Heroku dynosunda çalışıyor, bu da bazı sıkıntıları beraberinde getiriyor.
    if HEROKU_APIKEY is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_APIKEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APPNAME:
            await ups.edit(
                '`[HEROKU MEMEZ] Güncelleyiciyi kullanabilmek için HEROKU_APPNAME değişkenini tanımlamalısın.`'
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APPNAME:
                heroku_app = app
                break
        if heroku_app is None:
            await ups.edit(
                f'{txt}\n`Heroku değişkenleri yanlış veya eksik tanımlanmış.`'
            )
            repo.__del__()
            return
        await ups.edit('`[HEROKU MEMEZ]\
                        \nUserBot Heroku dynosuna aktarılıyor, lütfen bekle...`'
                       )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_APIKEY + "@")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except GitCommandError as error:
            await ups.edit(f'{txt}\n`Karşılaşılan hatalar burada:\n{error}`')
            repo.__del__()
            return
        await ups.edit('`Güncelleme başarıyla tamamlandı!\n'
                       'Yeniden başlatılıyor...`')
    else:
        # Klasik güncelleyici, oldukça basit.
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await update_requirements()
        await ups.edit('`Güncelleme başarıyla tamamlandı!\n'
                       'Yeniden başlatılıyor...`')
        # Bot için Heroku üzerinde yeni bir instance oluşturalım.
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        return

CMD_HELP.update({
    'update':
    ".update\
\nKullanım: Botunuza siz kurduktan sonra herhangi bir güncelleme gelip gelmediğini kontrol eder.\
\n\n.update now\
\nKullanım: Botunuzu günceller."
})
