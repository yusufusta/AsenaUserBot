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

# @NaytSeyd tarafından portlanmıştır.

from userbot import CMD_HELP, bot
from userbot.events import register
from urllib3 import PoolManager
from json import loads as jsloads


@register(outgoing=True, pattern="^.covid$")
async def covid(event):
    try:
        url = 'http://67.158.54.51/corona.php'
        http = PoolManager()
        request = http.request('GET', url)
        result = jsloads(request.data.decode('utf-8'))
        http.clear()
    except:
        await event.edit("`Bir hata oluştu.`")
        return

    sonuclar = ("** Koronavirüs Verileri **\n" +
                "\n**Dünya geneli**\n" +
                f"**🌎 Vaka:** `{result['tum']}`\n" +
                f"**🌎 Ölüm:** `{result['tumolum']}`\n" +
                f"**🌎 İyileşen:** `{result['tumk']}`\n" +
                "\n**Türkiye**\n" +
                f"**🇹🇷 Vaka (toplam):** `{result['trtum']}`\n" +
                f"**🇹🇷 Vaka (bugün):** `{result['trbtum']}`\n" +
                f"**🇹🇷 Vaka (aktif):** `{result['tra']}`\n" +
                f"**🇹🇷 Ölüm (toplam):** `{result['trolum']}`\n" +
                f"**🇹🇷 Ölüm (bugün):** `{result['trbolum']}`\n" +
                f"**🇹🇷 İyileşen:** `{result['trk']}`")

    await event.edit(sonuclar)


CMD_HELP.update({
    "covid19":
    ".covid \
    \nKullanım: Hem Dünya geneli hem de Türkiye için güncel Covid 19 istatistikleri."
})
