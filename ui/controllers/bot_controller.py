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
        # todo: this functionally works but is not correct and causes errors
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.stop_async())
        loop.close()

    async def stop_async(self):
        await self.bot.close()
