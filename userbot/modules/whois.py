# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


""" Telegram'daki herhangi bir kullanıcı hakkında bilgi almak için UserBot modülü (sizde dahil!). """

import os

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("whois")

# ████████████████████████████████ #

@register(pattern=".whois(?: |$)(.*)", outgoing=True)
async def who(event):
    await event.edit(
        LANG['GETTING_DATA'])

    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)

    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        return event.edit(LANG['FAILED_GETTING_DATA'])
        
    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await event.client.send_file(event.chat_id,
                                     photo,
                                     caption=caption,
                                     link_preview=False,
                                     force_document=False,
                                     reply_to=message_id_to_reply,
                                     parse_mode="html")

        if not photo.startswith("http"):
            os.remove(photo)
        await event.delete()

    except TypeError:
        await event.edit(caption, parse_mode="html")


async def get_user(event):
    """ Kullanıcıyı argümandan veya yanıtlanan mesajdan alın. """
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user


async def fetch_info(replied_user, event):
    """ Kullanıcı nesnesinden ayrıntıları alın. """
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.user.id,
                             offset=42,
                             max_id=0,
                             limit=80))
    replied_user_profile_photos_count = LANG['NO_PROFILE_PHOTO']
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError as e:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = LANG['NO_DC_ID']
        location = str(e)
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    photo = await event.client.download_profile_photo(user_id,
                                                      TEMP_DOWNLOAD_DIRECTORY +
                                                      str(user_id) + ".jpg",
                                                      download_big=True)
    first_name = first_name.replace(
        "\u2060", "") if first_name else (LANG['NO_FIRST_NAME'])
    last_name = last_name.replace(
        "\u2060", "") if last_name else (LANG['NO_LAST_NAME'])
    username = "@{}".format(username) if username else (
        LANG['NO_USERNAME'])
    user_bio = LANG['NO_BIO'] if not user_bio else user_bio

    caption = f"<b>{LANG['USER_INFO']}:</b>\n\n"
    caption += f"{LANG['NAME']}: {first_name}\n"
    caption += f"{LANG['LASTNAME']}: {last_name}\n"
    caption += f"{LANG['NICKNAME']}: {username}\n"
    caption += f"{LANG['DC_ID']}: {dc_id}\n"
    caption += f"{LANG['PROFILE_PHOTO_COUNT']}: {replied_user_profile_photos_count}\n"
    caption += f"{LANG['IS_BOT']}: {is_bot}\n"
    caption += f"{LANG['IS_RESTRICTED']}: {restricted}\n"
    caption += f"{LANG['IS_VERIFIED']}: {verified}\n"
    caption += f"ID: <code>{user_id}</code>\n\n"
    caption += f"{LANG['BIO']}: \n<code>{user_bio}</code>\n\n"
    caption += f"{LANG['COMMON_CHAT']}: {common_chat}\n"
    caption += f"{LANG['LINK']}: "
    caption += f"<a href=\"tg://user?id={user_id}\">{first_name}</a>"

    return photo, caption

CmdHelp('whois').add_command(
    'whois', ' <kullanıcı adı/yanıt/id>', 'Kullanıcının bilgilerini alır.'
).add()