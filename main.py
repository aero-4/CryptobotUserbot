import asyncio
import re

from telethon import TelegramClient, functions
from telethon.events.newmessage import NewMessage

SESSION = '123.session'
device = {"app_id": 2040,
          "app_hash": "b18441a1ff607e10a989891a5462e627",
          "device": "GOYK-EXTREME",
          "sdk": "Windows 10",
          "app_version": "5.10.7 x64",
          "system_lang_pack": "en",
          "system_lang_code": "en"}

client = TelegramClient(session=SESSION, api_id=device["app_id"], api_hash=device["app_hash"], lang_code=device["system_lang_code"], device_model=device["device"], system_version=device["sdk"])


def validation(text: str):
    if not text or not isinstance(text, str):
        return None
    for i in ["CryptoBot", "send", "calc"]:
        URL_PATTERN = re.compile(fr"(?:https?://)?t\.me/{i}\?start=([^&\s]*)")
        current = re.search(URL_PATTERN, text)
        if current is not None:
            return current.group(1)
        return None


async def check_exist(msg: str):
    try:
        bot = "@send"
        start_param = validation(msg)

        if start_param:
            await client(functions.contacts.UnblockRequest(bot))
            result = await client(functions.messages.StartBotRequest(
                bot=bot,
                peer=bot,
                start_param=start_param,
            ))
            print(f"Activated {start_param}")
        else:
            print("Not check")
    except Exception as e:
        print(f"Error: {e}")


@client.on(NewMessage())
async def get_checks(message):
    msg = getattr(message, 'message')
    if msg:
        await check_exist(msg.message)


async def main():
    async with client:
        me = await client.get_me()
        print(f"Work: {me.id} , @{me.username} , {me.phone}")
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
