# Standard Library
import asyncio
import datetime
import json
import logging
import os
import re
from enum import Enum
from urllib import request as url_request

# Third-Party
import requests as req
import spotipy
from pydantic import ValidationError
from spotipy.oauth2 import SpotifyOAuth
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.types import AuthScope
from twitchio import Message, Chatter, Channel
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.stringparser import StringParser

# Local
from bot.blacklists import read_json, write_json
from constants import CACHE, CONFIG, Permission
from ui.models.config import Config


def _require_permissions(ctx, permission_set):
    """
    RBAC for commands

    :param ctx: context param from twitchio
    :param permission_set: list of permission strings
    :return: boolean (allow or disallow run)
    """

    for permission in permission_set:
        if permission.value in ctx.author.badges:
            return True

    return False


class Bot(commands.Bot):
    def __init__(self):
        with open(CONFIG) as config_file:
            config_data = json.load(config_file)
        try:
            self.config = Config(**config_data)
        except ValidationError:
            self.config = Config()
        super().__init__(
            token=self.config.token,
            client_id=self.config.client_id,
            nick=self.config.nickname,
            prefix=self.config.prefix,
            initial_channels=[self.config.channel],
            case_insensitive=True
        )

        self.token = os.environ.get("SPOTIFY_AUTH")
        self.version = "0.2"

        self.request_history = {}
        self.last_song = None

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.config.spotify_client_id,
                client_secret=self.config.spotify_secret,
                redirect_uri="http://localhost:8080",
                cache_path=CACHE,
                scope=[
                    "user-modify-playback-state",
                    "user-read-currently-playing",
                    "user-read-playback-state",
                    "user-read-recently-played",
                ],
            )
        )

        self.URL_REGEX = (
            r"(?i)\b("
            r"(?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"
            r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+"
            r"(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|"
            r"[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        )

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
        await ctx.send(
            f":) 🎶 ScryptTunes v{self.version} is online!"
        )

    @commands.command(name="blacklistuser")
    async def blacklist_user(self, ctx, *, user: str):
        user = user.lower()
        if ctx.author.is_mod:
            file = read_json("blacklist_user")
            if user not in file["users"]:
                file["users"].append(user)
                write_json(file, "blacklist_user")
                await ctx.send(f"{user} added to blacklist")
            else:
                await ctx.send(f"{user} is already blacklisted")
        else:
            await ctx.send("You don't have permission to do that.")

    @commands.command(name="unblacklistuser")
    async def unblacklist_user(self, ctx, *, user: str):
        user = user.lower()
        if ctx.author.is_mod:
            _file = read_json("blacklist_user")
            if user in _file["users"]:
                _file["users"].remove(user)
                write_json(_file, "blacklist_user")
                await ctx.send(f"{user} removed from blacklist")
            else:
                await ctx.send(f"{user} is not blacklisted")
        else:
            await ctx.send("You don't have permission to do that.")

    @commands.command(name="blacklist", aliases=["blacklistsong", "blacklistadd"])
    async def blacklist_command(self, ctx, *, song_uri: str):
        if ctx.author.is_mod:
            jscon = read_json("blacklist")

            song_uri = song_uri.replace("spotify:track:", "")

            if song_uri not in jscon["blacklist"]:
                if re.match(self.URL_REGEX, song_uri):
                    data = self.sp.track(song_uri)
                    song_uri = data["uri"]
                    song_uri = song_uri.replace("spotify:track:", "")

                track = self.sp.track(song_uri)

                track_name = track["name"]

                jscon["blacklist"].append(song_uri)

                write_json(jscon, "blacklist")

                await ctx.send(f"Added {track_name} to blacklist.")

            else:
                await ctx.send("Song is already blacklisted.")

        else:
            await ctx.send("You are not authorized to use this command.")

    @commands.command(
        name="unblacklist", aliases=["unblacklistsong", "blacklistremove"]
    )
    async def unblacklist_command(self, ctx, *, song_uri: str):
        if ctx.author.is_mod:
            jscon = read_json("blacklist")

            song_uri = song_uri.replace("spotify:track:", "")

            if re.match(self.URL_REGEX, song_uri):
                data = self.sp.track(song_uri)
                song_uri = data["uri"]
                song_uri = song_uri.replace("spotify:track:", "")

            if song_uri in jscon["blacklist"]:
                jscon["blacklist"].remove(song_uri)
                write_json(jscon, "blacklist")
                await ctx.send("Removed that song from the blacklist.")

            else:
                await ctx.send("Song is not blacklisted.")
        else:
            await ctx.send("You are not authorized to use this command.")

    @commands.command(name="np", aliases=["nowplaying", "song"])
    async def np_command(self, ctx):
        data = self.sp.currently_playing()
        song_artists = data["item"]["artists"]
        song_artists_names = [artist["name"] for artist in song_artists]

        min_through = int(data["progress_ms"] / (1000 * 60) % 60)
        sec_through = int(data["progress_ms"] / (1000) % 60)
        time_through = f"{min_through} mins, {sec_through} secs"

        min_total = int(data["item"]["duration_ms"] / (1000 * 60) % 60)
        sec_total = int(data["item"]["duration_ms"] / (1000) % 60)
        time_total = f"{min_total} mins, {sec_total} secs"

        logging.info(
            f"🎶Now Playing - {data['item']['name']} by {', '.join(song_artists_names)} | Link: {data['item']['external_urls']['spotify']} | {time_through} - {time_total}")
        await ctx.send(
            f"🎶Now Playing - {data['item']['name']} by {', '.join(song_artists_names)} | Link: {data['item']['external_urls']['spotify']} | {time_through} - {time_total}"
        )

    @commands.command(
        name="lastsong", aliases=["previoussongs", "last", "previousplayed"]
    )
    async def recent_played_command(self, ctx):
        recents = self.sp.current_user_recently_played(limit=10)
        songs = []

        for song in recents["items"]:
            # if the song artists include more than one artist: add all artist names to an artist list variable
            if len(song["track"]["artists"]) > 1:
                artists = [artist["name"] for artist in song["track"]["artists"]]
                song_artists = ", ".join(artists)
            # if the song artists only include one artist: add the artist name to the artist list variable
            else:
                song_artists = song["track"]["artists"][0]["name"]

            songs.append(song["track"]["name"] + " - " + song_artists)

        logging.info("Recently Played: " + " | ".join(songs))
        await ctx.send("Recently Played: " + " | ".join(songs))

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
        if self.last_song:
            queue = self.sp.queue()
            current_playback = self.sp.current_playback()

            total_songs = 1
            playlist_time_remaining = current_playback['item']['duration_ms'] - current_playback['progress_ms']

            for song in queue['queue'][::-1]:
                last_song_found = False
                if song['id'] == self.last_song:
                    last_song_found = True
                if last_song_found:
                    total_songs += 1
                    playlist_time_remaining += song['duration_ms']

            total_seconds = playlist_time_remaining // 1000
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            await ctx.send(f'Songs In Queue: {total_songs}'
                           f'| Next added song would play in: {hours} hours {minutes:02}:{seconds:02} minutes')
        else:
            await ctx.send(f'Queue is empty!')

    @commands.command(name="srhelp", aliases=[])
    async def help_command(self, ctx):
        await ctx.send("!sr <song name + artist or Spotify URL> - "
                       "Request a song to be added to the queue. "
                       "Example: !sr Never Gonna Give You Up - Rick Astley")

    @commands.command(name="songrequest", aliases=["sr", "addsong"])
    async def songrequest_command(self, ctx, *, song: str = None):

        if not song:
            return await self.help_command(ctx)

        try:
            song_uri = None

            if (
                    song.startswith("spotify:track:")
                    or not song.startswith("spotify:track:")
                    and re.match(self.URL_REGEX, song)
            ):
                song_uri = song
                await self.chat_song_request(ctx, song_uri, song_uri, album=False)

            else:
                await self.chat_song_request(ctx, song, song_uri, album=False)
        except Exception as e:
            # todo: ctx.send different messages based on error type/contents
            logging.error(f"{e}")
            await ctx.send(f"@{ctx.author.name}, there was an error with your request!")

    # @commands.command(name="skip")
    # async def skip_song_command(self, ctx):
    #     sp.next_track()
    #     await ctx.send(f":) 🎶 Skipping song...")

    # @commands.command(name="albumqueue")
    #     if ctx.author.is_mod or ctx.author.is_subscriber:
    # async def albumqueue_command(self, ctx, *, album: str):
    #         album_uri = None

    #         if (
    #             album.startswith("spotify:album:")
    #             or not album.startswith("spotify:album:")
    #             and re.match(self.URL_REGEX, album)
    #         ):
    #             album_uri = album
    #         await self.album_request(ctx, album_uri)
    #     else:
    #         await ctx.send(f"🎶You don't have permission to do that! (Album queue is Sub Only!)")

    """
        DO NOT USE THE API REQUEST IT WONT WORK.
        the logic should still work iwth using the spotipy library, so thats why I'm keeping it, but don't do an API request
        - like this.
    """

    # async def album_request(self, ctx, song):
    #     song = song.replace("spotify:album:", "")
    #     ALBUM_URL = f"https://api.spotify.com/v1/albums/{song}?market=US"
    #     async with request("GET", ALBUM_URL, headers={
    #                 "Content-Type": "application/json",
    #                 "Authorization": "Bearer " + self.token,
    #             }) as resp:
    #             data = await resp.json()
    #             songs_uris = [artist["uri"] for artist in data['tracks']['items']]

    #             for song_uris in songs_uris:
    #                 await self.song_request(ctx, song, song_uris, album=True)
    #             await ctx.send(f"Album Requested! {data['name']}")
    #             return

    async def chat_song_request(self, ctx, song, song_uri, album: bool, requests=None):
        blacklisted_users = read_json("blacklist_user")["users"]
        if ctx.author.name.lower() in blacklisted_users:
            logging.warning(f"Blacklisted user @{ctx.author.name} attempted request: Song:{song} - URI:{song_uri}")
            await ctx.send("You are blacklisted from requesting songs.")
        else:
            jscon = read_json("blacklist")

            if song_uri is None:
                data = self.sp.search(song, limit=1, type="track", market="US")
                song_uri = data["tracks"]["items"][0]["uri"]

            elif re.match(self.URL_REGEX, song_uri):
                if 'spotify' in song_uri:
                    if '.link/' in song_uri:  # todo: better way to handle this?
                        ctx.send(
                            f'{ctx.author} Mobile link detected, attempting to get full url.')  # todo: verify this is sending?????
                        req_data = req.get(
                            song_uri,
                            allow_redirects=True,
                            headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                              'like Gecko) Chrome/119.0.0.0 Safari/537.36'
                            }

                        )
                        data = self.sp.track(req_data.url)
                    else:
                        data = self.sp.track(song_uri)
                    song_uri = data["uri"]
                    song_uri = song_uri.replace("spotify:track:", "")
                if 'youtube' in song_uri or 'youtu.be' in song_uri:
                    with url_request.urlopen('https://noembed.com/embed?url=' + song_uri) as url:
                        data = json.load(url)
                        title, author = data['title'], data['author_name']
                    logging.info(f"Youtube Link Detected <{song_uri}> - Searching song name on Spotify as fallback")
                    await ctx.send(f"Youtube Link Detected - Searching song name on Spotify as fallback")
                    await self.chat_song_request(ctx, f'{title} {author}', song_uri=None, album=False)
                    return

            song_id = song_uri.replace("spotify:track:", "")

            if not album:
                data = self.sp.track(song_id)
                song_name = data["name"]
                song_artists = data["artists"]
                song_artists_names = [artist["name"] for artist in song_artists]
                duration = data["duration_ms"] / 60000

            if song_uri != "not found":
                if song_id in jscon["blacklist"]:
                    logging.warning(f"User @{ctx.author.name} requested blacklisted song: {song_id}")
                    return await ctx.send(f"@{ctx.author.name} That song is blacklisted.")

                if duration > 17:
                    return await ctx.send(f"@{ctx.author.name} Send a shorter song please! :3")

                if self.config.rate_limit:
                    if ctx.author in self.request_history:
                        if (datetime.datetime.now() - self.request_history[ctx.author][
                            "last_request_time"]).seconds < 300:
                            return await ctx.send(f"@{ctx.author.name} You need to wait 10 minutes between requests!")

                        self.request_history[ctx.author]["last_request_time"] = datetime.datetime.now()
                        self.request_history[ctx.author]["last_requested_song_id"] = song_id
                        self.last_song = song_id
                    else:
                        self.request_history[ctx.author] = {
                            "last_request_time": datetime.datetime.now(),
                            "last_requested_song_id": song_id
                        }
                        self.last_song = song_id

                self.sp.add_to_queue(song_uri)
                logging.info(
                    f"Song successfully added to queue: ({song_name} by {', '.join(song_artists_names)}) [ {data['external_urls']['spotify']} ]")
                await ctx.send(
                    f"@{ctx.author.name}, Your song ({song_name} by {', '.join(song_artists_names)}) [ {data['external_urls']['spotify']} ] has been added to the queue!"
                )
