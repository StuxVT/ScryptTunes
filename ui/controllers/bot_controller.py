import asyncio
import logging
import threading
from typing import Optional
from datetime import datetime, timedelta

class ResilientBot(Bot):
    def __init__(self):
        super().__init__()
        self.last_reconnect_attempt = None
        self.reconnect_cooldown = 30
        self.is_connected = False
        self._reconnect_task: Optional[asyncio.Task] = None
        
    async def run(self):
        while True:
            try:
                self.is_connected = False
                await super().run()
            except Exception as e:
                logging.error(f"Bot disconnected with error: {str(e)}")
                await self._handle_disconnect()
            
    async def _handle_disconnect(self):
        """Handle disconnection with exponential backoff."""
        if self.last_reconnect_attempt:
            time_since_last_attempt = (datetime.now() - self.last_reconnect_attempt).total_seconds()
            if time_since_last_attempt < self.reconnect_cooldown:
                await asyncio.sleep(self.reconnect_cooldown - time_since_last_attempt)
        
        self.last_reconnect_attempt = datetime.now()
        logging.info("Attempting to reconnect...")

    async def event_ready(self):
        """Override the existing event_ready to track connection status"""
        self.is_connected = True
        self.last_reconnect_attempt = None
        await super().event_ready()

class BotController:
    def __init__(self, root):
        self.root = root
        self.async_thread = None
        self.bot_run_event = asyncio.Event()
        self.loop = asyncio.new_event_loop()
        self.bot: Optional[ResilientBot] = None
        self._health_check_task: Optional[asyncio.Task] = None

    def start(self):
        if not self.bot_run_event.is_set():
            self.bot_run_event.set()
            if self.loop.is_closed():
                self.loop = asyncio.new_event_loop()
            self.async_thread = threading.Thread(target=self._run)
            self.async_thread.start()

    def stop(self):
        logging.info("Stopping bot gracefully...")
        self.bot_run_event.clear()
        if self._health_check_task:
            self.loop.call_soon_threadsafe(self._health_check_task.cancel)
        self.loop.call_soon_threadsafe(self.loop.stop)
        
    async def _health_check(self):
        """Periodic health check to monitor bot status"""
        while self.bot_run_event.is_set():
            if self.bot and not self.bot.is_connected:
                logging.warning("Bot disconnected, triggering reconnection...")
            await asyncio.sleep(30)

    def _run(self):
        asyncio.set_event_loop(self.loop)
        self.bot = ResilientBot()
        self._health_check_task = self.loop.create_task(self._health_check())
        self.loop.create_task(self.bot.run())
        self.loop.run_forever()