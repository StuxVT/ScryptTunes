import logging
import re
from typing import List
import json
import datetime
from urllib import request as url_request


# Third Party
import requests as req
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Local
from constants import CACHE
from bot.utils.blacklists import read_json, is_user_blacklisted, is_song_blacklisted
from bot.utils.spotify_utils import get_song_details


class SpotifyCommands:
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 redirect_uri: str = "https://localhost:8080",
                 spotify_scopes: List[str] = None,
                 rate_limit: int = 0):

        if spotify_scopes is None:
            # Avoid mutability of default value with this
            spotify_scopes = [
                "user-modify-playback-state",
                "user-read-currently-playing",
                "user-read-playback-state",
                "user-read-recently-played",
            ]

        if client_id is None:
            logging.critical("No spotify client id provided")
            raise ValueError("client_id must be set")

        if client_secret is None:
            logging.critical("No spotify client secret provided")
            raise ValueError("client_secret must be set")

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.spotify_scopes = spotify_scopes

        self.rate_limit = rate_limit

        self.spotipy_instance = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
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

        self.request_history = {}
        self.last_song = None

    async def chat_song_request(self, ctx, song, song_uri, album: bool, requests= None):
        # todo: why is there a requests argument here?
        if is_user_blacklisted(ctx.author.name):
            logging.warning(f"Blacklisted user @{ctx.author.name} attempted request: Song:{song} - URI:{song_uri}")
            await ctx.send("You are blacklisted from requesting songs.")
            return

        song_uri = await self.handle_song_uri(ctx, song, song_uri)
        if not song_uri:
            return

        song_id = song_uri.replace("spotify:track:", "")
        await self.process_song_request(ctx, song_uri, song_id, album)

    async def handle_song_uri(self, ctx, song, song_uri) -> str:
        """
        Handles song URI, parses it and gets a spotify song URI.
        """
        if song_uri is None:
            song_details = get_song_details(self.spotipy_instance, song)
            return song_details["tracks"]["items"][0]["uri"]

        if re.match(self.URL_REGEX, song_uri):
            return await self.handle_external_links(ctx, song_uri)

    async def handle_external_links(self, ctx, song_uri):
        """
        Standardizes external links
        """
        if "spotify" in song_uri:
            return self.handle_spotify_link(ctx, song_uri)
        if "youtube" in song_uri:
            return await self.handle_youtube_link(ctx, song_uri)

    async def handle_spotify_link(self, ctx, song_uri):
        """
        Handles spotify links
        """
        if '.link/' in song_uri:  # todo: better way to handle this?
            # Handle mobile links
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
            data = self.spotipy_instance.track(req_data.url)
        else:
            data = self.spotipy_instance.track(song_uri)

        return data["uri"].replace("spotify:track:", "")

    async def handle_youtube_link(self, ctx, song_uri):
        logging.info(f"Youtube Link Detected <{song_uri}> - Searching song name on Spotify as fallback")
        await ctx.send("Youtube Link Detected - Searching song name on Spotify as fallback")
        with url_request.urlopen('https://noembed.com/embed?url=' + song_uri) as url:
            data = json.load(url)
            title, author = data['title'], data['author_name']
        song_details = get_song_details(self.spotipy_instance, f'{title} {author}')
        return song_details["tracks"]["items"][0]["uri"]

    async def process_song_request(self, ctx, song_uri, song_id, album):
        if not album:
            data = self.spotipy_instance.track(song_id)
            song_name = data["name"]
            song_artists = data["artists"]
            song_artists_names = [artist["name"] for artist in song_artists]
            duration = data["duration_ms"] / 60000

        if song_uri == "not found":
            return

        if is_song_blacklisted(song_id):
            logging.warning(f"User @{ctx.author.name} requested blacklisted song: {song_id}")
            return await ctx.send(f"@{ctx.author.name} That song is blacklisted.")

        if duration > 17:
            # todo: I am not 100% sure why this is hardcoded like this
            logging.warning(f"User @{ctx.author.name} requested song duration: {duration} seconds, which is more than allowed.")
            return await ctx.send(f"@{ctx.author.name} Send a shorter song please! :3")

        if not self.handle_rate_limiter(ctx, song_id):
            return

        self.spotipy_instance.add_to_qeue(song_uri)
        logging.info(
            f"Song successfully added to queue: ({song_name} by {', '.join(song_artists_names)}) [ {data['external_urls']['spotify']} ]")
        await ctx.send(
            f"@{ctx.author.name}, Your song ({song_name} by {', '.join(song_artists_names)}) [ {data['external_urls']['spotify']} ] has been added to the queue!"
        )

    async def handle_rate_limiter(self, ctx, song_id) -> bool:
        if ctx.author in self.request_history:
            if (datetime.datetime.now() - self.request_history[ctx.author][
                "last_request_time"]).seconds < 300:
                # todo: This should not be hardcorded

                # todo: This also states in the ctx.send that it needs to be 10 minutes, but the if statement
                #  specifies 5? (I am not changing since this is just a rewrite)
                await ctx.send(f"@{ctx.author.name} You need to wait 10 minutes between requests!")
                return False
            self.request_history[ctx.author]["last_request_time"] = datetime.datetime.now()
            self.request_history[ctx.author]["last_requested_song_id"] = song_id
            self.last_song = song_id
            return True
        self.request_history[ctx.author] = {
            "last_request_time": datetime.datetime.now(),
            "last_requested_song_id": song_id
        }
        self.last_song = song_id
        return True



