import asyncio
import logging
import threading

from bot.scrypt_tunes import Bot


class BotController:
    def __init__(self, root):
        self.root = root
        self.async_thread = None
        self.bot_run_event = asyncio.Event()
        self.loop = asyncio.new_event_loop()

    def start(self):
        if not self.bot_run_event.is_set():
            self.bot_run_event.set()
            if self.loop.is_closed():
                self.loop = asyncio.new_event_loop()
            self.async_thread = threading.Thread(target=self._run)
            self.async_thread.start()

    def stop(self):
        logging.info(
            f"---------------------------------------------------\n"
            f"Asking bot nicely to commit die"
        )
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.bot_run_event.clear()

    def _run(self):
        asyncio.set_event_loop(self.loop)
        self.bot = self.loop.create_task(Bot().run())
        self.loop.run_forever()
