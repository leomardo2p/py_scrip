import asyncio
from telethon import TelegramClient # type: ignore
from telethon import functions
from telethon.tl.types import *

#Mis_datos
api_id = 29068923
api_hash = '72035fc7d10fc5bd2847e23ecad1a850'
client = TelegramClient("anon",api_id,api_hash)


async def main():
    
    while (True):
        await client.send_message("@automaticsubscripbot","/ver")
        await asyncio.sleep(86400)
        print("A dormir 24 horas")
        
with client:
    client.loop.run_until_complete(main())