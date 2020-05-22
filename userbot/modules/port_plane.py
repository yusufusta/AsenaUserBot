#By STARKTM1
from telethon import events
import asyncio
import os
import sys
from userbot.events import register

@register(outgoing=True, pattern="^.plane")
async def port_plane(event):
    if event.fwd_from:
        return
        
        
    await event.edit("✈-------------")
    await asyncio.sleep(1)
    await event.edit("-✈------------")
    await asyncio.sleep(1)
    await event.edit("--✈-----------")
    await asyncio.sleep(1)
    await event.edit("---✈----------")
    await asyncio.sleep(1)
    await event.edit("----✈---------")
    await asyncio.sleep(1)
    await event.edit("-----✈--------")
    await asyncio.sleep(1)
    await event.edit("------✈-------")
    await asyncio.sleep(1)
    await event.edit("-------✈------")
    await asyncio.sleep(1)
    await event.edit("--------✈-----")
    await asyncio.sleep(1)
    await event.edit("---------✈----")
    await asyncio.sleep(1)
    await event.edit("----------✈---")
    await asyncio.sleep(1)
    await event.edit("-----------✈--")
    await asyncio.sleep(1)
    await event.edit("------------✈-")
    await asyncio.sleep(1)
    await event.edit("-------------✈")
    await asyncio.sleep(5)
    await event.delete()

