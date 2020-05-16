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

""" Sed için UserBot modülü """

import re
from sre_constants import error as sre_err
from userbot import CMD_HELP
from asyncio import sleep
from userbot.events import register

DELIMITERS = ("/", ":", "|", "_")


async def separate_sed(sed_string):
    """ Sed argümanları. """

    if len(sed_string) < 2:
        return

    if (len(sed_string) >= 2 and sed_string[2] in DELIMITERS
            and sed_string.count(sed_string[2]) >= 2):
        delim = sed_string[2]
        start = counter = 3
        while counter < len(sed_string):
            if sed_string[counter] == "\\":
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None

        while counter < len(sed_string):
            if (sed_string[counter] == "\\" and counter + 1 < len(sed_string)
                    and sed_string[counter + 1] == delim):
                sed_string = sed_string[:counter] + sed_string[counter + 1:]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ""

        flags = ""
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()
    return None


@register(outgoing=True, pattern="^.s")
async def sed(command):
    """ Sed komutu için Telegram'da sed kullanın. """
    sed_result = await separate_sed(command.text)
    textx = await command.get_reply_message()
    if sed_result:
        if textx:
            to_fix = textx.text
        else:
            await command.edit(
                "`Bunun için yeterli zekâya sahip değilim.`")
            return

        repl, repl_with, flags = sed_result

        if not repl:
            await command.edit(
                "`Bunun için yeterli zekâya sahip değilim.`")
            return

        try:
            check = re.match(repl, to_fix, flags=re.IGNORECASE)
            if check and check.group(0).lower() == to_fix.lower():
                await command.edit("`Bu bir yanıtlama. Sed kullanma`")
                return

            if "i" in flags and "g" in flags:
                text = re.sub(repl, repl_with, to_fix, flags=re.I).strip()
            elif "i" in flags:
                text = re.sub(repl, repl_with, to_fix, count=1,
                              flags=re.I).strip()
            elif "g" in flags:
                text = re.sub(repl, repl_with, to_fix).strip()
            else:
                text = re.sub(repl, repl_with, to_fix, count=1).strip()
        except sre_err:
            await command.edit("Dostum lütfen [regex](https://regexone.com) öğren!")
            return
        if text:
            await command.edit(f"Bunu mu demek istedin ? \n\n{text}")


CMD_HELP.update({
    "sed":
    ".s<sınırlayıcı><eski kelime(ler)><sınırlayıcı><yeni kelime(ler)>\
    \nKullanım: Sed kullanarak bir kelimeyi veya kelimeleri değiştirir.\
    \nSınırlayıcılar: `/, :, |, _`"
})
