import asyncio
import logging
import threading
import ctypes
import time

from bot.scrypt_tunes import Bot


def _terminate_thread(thread):
    """Terminates a python thread from another thread."""
    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

    # Wait for the thread to actually terminate
    thread.join(timeout=5)
    if thread.is_alive():
        logging.warning("Failed to terminate thread")


class BotController:
    def __init__(self, root):
        self.root = root
        self.async_thread = None
        self.bot_run_event = asyncio.Event()
        self.loop = asyncio.new_event_loop()
        self.bot = None

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
            f"Forcefully stopping the bot"
        )
        self.bot_run_event.clear()

        # Stop the asyncio loop
        self.loop.call_soon_threadsafe(self.loop.stop)

        # Wait for a short time to allow for clean shutdown
        time.sleep(1)

        # If the thread is still alive, terminate it forcefully
        if self.async_thread and self.async_thread.is_alive():
            _terminate_thread(self.async_thread)

        # Close the loop
        self.loop.close()

    def _run(self):
        asyncio.set_event_loop(self.loop)
        self.bot = Bot()
        # Run the bot
        self.bot_task = self.loop.create_task(self.bot.start())
        # Setup PubSub
        # self.loop.run_until_complete(self.bot.setup_pubsub())

        self.loop.run_forever()

