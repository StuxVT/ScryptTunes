import logging
import threading
import asyncio

from bot.scrypt_tunes import Bot


class BotController:
    def __init__(self):
        self.bot = Bot()
        self.bot_thread = threading.Thread(target=self.bot.run)

    def start(self):
        if not self.bot_thread.is_alive():
            self.bot_thread.start()
        else:
            logging.info("Bot already started")

    def stop(self):
        pass

    async def stop_async(self):
        await self.bot.close()
