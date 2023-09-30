import json
import os
import re
import logging

from twitchio.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from urllib import request as url_request

from bot.blacklists import read_json, write_json, is_blacklisted
from constants import CONFIG, CACHE


class Bot(commands.Bot):
    def __init__(self):
        with open(CONFIG) as config_file:
            config = json.load(config_file)
        super().__init__(
            token=config.get("token"),
            client_id=config.get("client_id"),
            nick=config["nickname"],
            prefix=config["prefix"],
            initial_channels=config["channels"],
        )

        self.token = os.environ.get("SPOTIFY_AUTH")
        self.version = "0.2"

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=config.get("spotify_client_id"),
                client_secret=config.get("spotify_secret"),
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

        self.URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
                         r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    async def event_ready(self):
        logging.info("\n" * 100)
        logging.info(f"ScryptTunes ({self.version}) Ready, logged in as: {self.nick}")

    def is_owner(self, ctx):
        return ctx.author.id == "640348450"

    @commands.command(name="ping", aliases=["ding"])
    async def ping_command(self, ctx):
        await ctx.send(
            f":) 🎶 ScryptTunes v{self.version} is online!"
        )

    @commands.command(name="blacklistuser")
    async def blacklist_user(self, ctx, *, user: str):
        user = user.lower()
        if ctx.author.is_mod or self.is_owner(ctx):
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
        if ctx.author.is_mod or self.is_owner(ctx):
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
        if ctx.author.is_mod or self.is_owner(ctx):
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
        if ctx.author.is_mod or self.is_owner(ctx):
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
    async def queue_command(self, ctx):
        queue = self.sp.current_user_recently_played(limit=10)
        songs = []

        for song in queue["items"]:
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

    @commands.command(name="songrequest", aliases=["sr", "addsong"])
    async def songrequest_command(self, ctx, *, song: str):
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
            await ctx.send(f"@{ctx.author.name}, spotify links only, or just type out the song/artist names please!")

    # @commands.command(name="skip")
    # async def skip_song_command(self, ctx):
    #     sp.next_track()
    #     await ctx.send(f":) 🎶 Skipping song...")

    # @commands.command(name="albumqueue")
    #     if ctx.author.is_mod or ctx.author.is_subscriber or self.is_owner(ctx):
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

    async def chat_song_request(self, ctx, song, song_uri, album: bool):
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
                    await ctx.send(f"@{ctx.author.name} That song is blacklisted.")

                elif duration > 17:
                    await ctx.send(f"@{ctx.author.name} Send a shorter song please! :3")
                else:
                    self.sp.add_to_queue(song_uri)
                    logging.info(
                        f"Song successfully added to queue: ({song_name} by {', '.join(song_artists_names)}) [ {data['external_urls']['spotify']} ]")
                    await ctx.send(
                        f"@{ctx.author.name}, Your song ({song_name} by {', '.join(song_artists_names)}) [ {data['external_urls']['spotify']} ] has been added to the queue!"
                    )
