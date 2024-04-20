# Standard Library
import asyncio
import datetime
import logging
import os
from enum import Enum

# Third-Party
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.types import AuthScope
from twitchio import Message, Chatter, Channel
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.stringparser import StringParser

from bot.commands.chat_commands import ChatCommands
from bot.commands.spotify_commands import SpotifyCommands
# Local
from bot.utils.blacklists import read_json
from bot.utils import get_bot_version, get_bot_config


class Permission(Enum):
    UNSUBBED = 1
    SUBBED = 2
    VIP = 3
    MOD = 4
    STREAMER = 5


class Bot(commands.Bot):
    def __init__(self):

        self.config = get_bot_config()

        super().__init__(
            token=self.config.token,
            client_id=self.config.client_id,
            nick=self.config.nickname,
            prefix=self.config.prefix,
            initial_channels=[self.config.channel],
        )

        self.token = os.environ.get("SPOTIFY_AUTH")
        self.version = get_bot_version()

        self.request_history = {}

        self.spotify_commands = SpotifyCommands(
            client_id=self.config.spotify_client_id,
            client_secret=self.config.spotify_secret,
            rate_limit=self.config.rate_limit
        )
        self.spotipy_instance = self.spotify_commands.spotipy_instance

    @staticmethod
    async def event_ready(self):
        if self.config.channel_points_reward:
            # Set up TwitchAPI Sub for Channel Point Redeems
            twitch = Twitch(self.config.client_id, self.config.client_secret)
            twitch.authenticate_app([])
            target_scope: list = [AuthScope.CHANNEL_READ_REDEMPTIONS]
            auth = UserAuthenticator(twitch, target_scope, force_verify=False)
            token, refresh_token = auth.authenticate()
            twitch.set_user_authentication(token, target_scope, refresh_token)

            user_id: str = twitch.get_users(logins=[self.config.channel])["data"][0]["id"]

            pubsub = PubSub(twitch)
            uuid = pubsub.listen_channel_points(user_id, self.channel_point_event)
            pubsub.start()

        logging.info("\n" * 100)
        logging.info(f"ScryptTunes ({self.version}) Ready, logged in as: {self.nick}")

    def channel_point_event(self, uuid, data):
        # TODO: ctx.send not working when invoking song requests through redeem
        if (
                data["data"]["redemption"]["reward"]["title"].lower()
                != self.config.channel_points_reward.lower()
        ):
            return

        song: str = data["data"]["redemption"]["user_input"]
        blacklisted_users = read_json("blacklist_user")["users"]
        if data["data"]["redemption"]["user"]["login"] in blacklisted_users:
            return

        # Create fake context for injection into song request event
        websocket = self._connection
        chatter = Chatter(
            websocket=websocket,  # todo
            name=data["data"]["redemption"]["user"]["login"],
            channel=data["data"]["redemption"]["channel_id"],
            tags={
                'user-id': data["data"]["redemption"]["user"]["id"],
                'subscriber': '0',  # todo
                'mod': '0',  # todo
                'display-name': data["data"]["redemption"]["user"]["display_name"],
                'color': '#000000',  # todo
                'vip': '0',  # todo
            }
        )
        message = Message(
            content=song,
            author=chatter,
            channel=Channel(name=data["data"]["redemption"]["channel_id"], websocket=websocket),
            tags={
                'id': data["data"]["redemption"]["id"],
                'tmi-sent-ts': datetime.datetime.now().timestamp() * 1000,
            }
        )
        view = StringParser()
        view.process_string(song)
        ctx = Context(
            message=message,
            bot=self,
            prefix=self.config.prefix,
            command=self.songrequest_command,
            args=[],  # n/a
            kwargs={},  # n/a
            valid=True,
            view=view
        )

        asyncio.run_coroutine_threadsafe(self.invoke(context=ctx), asyncio.get_event_loop())

    @commands.command(name="ping", aliases=["ding"])
    async def ping_command(self, ctx):
        await ChatCommands.ping(ctx, self.version)

    @commands.command(name="songrequest", aliases=["sr", "addsong"])
    async def songrequest_command(self, ctx, *, song: str = None):
        song, song_uri = await ChatCommands.song_request(ctx, song)
        if song is None:
            return
        await self.spotify_commands.chat_song_request(ctx, song, song_uri, False)

    @commands.command(name="srhelp", aliases=[])
    async def help_command(self, ctx):
        await ChatCommands._help(ctx)
    @commands.command(name="blacklistuser")
    async def blacklist_user(self, ctx, *, user: str):
        await ChatCommands.blacklist_user(ctx, user)

    @commands.command(name="unblacklistuser")
    async def unblacklist_user(self, ctx, *, user: str):
        await ChatCommands.unblacklist_user(ctx, user)

    @commands.command(name="blacklist", aliases=["blacklistsong", "blacklistadd"])
    async def blacklist_command(self, ctx, *, song_uri: str):
        await ChatCommands.blacklist_song(ctx, song_uri)

    @commands.command(
        name="unblacklist", aliases=["unblacklistsong", "blacklistremove"]
    )
    async def unblacklist_command(self, ctx, *, song_uri: str):
        await ChatCommands.unblacklist_song(ctx, song_uri)

    @commands.command(name="np", aliases=["nowplaying", "song"])
    async def np_command(self, ctx):
        await ChatCommands.now_playing(ctx, self.spotipy_instance)
    @commands.command(
        name="lastsong", aliases=["previoussongs", "last", "previousplayed"]
    )
    async def recent_played_command(self, ctx):
        await ChatCommands.recently_played(ctx, self.spotipy_instance)

    @commands.command(
        name="queue", aliases=[]
    )
    async def queue_command(self, ctx):
        """
        TODO: Handle case where user cares about "when is my song gonna play?"
            - need to keep track of entire user's playback history
            - can probably implement this when playlistqueue is implemented and
                piggyback off its playback state watcher to update the user's request history

        TODO: breaks if queue size greater than 20

        :param ctx:
        :return:
        """
        await ChatCommands.queue(ctx, self.spotipy_instance, self.spotify_commands.last_song)



