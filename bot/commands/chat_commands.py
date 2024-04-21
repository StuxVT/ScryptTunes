import logging
import re
from typing import Tuple

from spotipy import Spotify
from twitchio.ext.commands import Context

# Third Party

from bot.utils import get_bot_config
from bot.utils.blacklists import (blacklist_user as register_blacklisted_user, unblacklist_user as remove_blacklist_of_user, blacklist_song as register_blacklisted_song,
                                  unblacklist_song as remove_blacklist_of_song)
from bot.utils.spotify_utils import get_track_name_from_uri, get_currently_playing_message, \
    get_recently_playing_message, get_queue_message


class ChatCommands:
    """
    Static class to handle chat commands
    (it is made like this so that it is easily recognizable in other files)
    """

    @staticmethod
    async def ping(ctx: Context, version: str) -> None:
        await ctx.send(
            f":) 🎶 ScryptTunes v{version} is online!"
        )

    @staticmethod
    async def song_request(ctx: Context,
                           song: str,
                           url_regex: str = (
            r"(?i)\b("
            r"(?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"
            r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+"
            r"(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|"
            r"[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")) -> Tuple[str, str] | Tuple[None, None]:

        """
        Handle a twitch song request
        Args:
            ctx: Context object of the message
            song: Song requested
            url_regex: (optional) Regex to match URLs for.

        Returns: (song, song_id) if successful, (None, None) otherwise. song_uri will be None if the param song was not
        a URL
        """

        if not song:
            await ChatCommands._help(ctx)
            return None, None
        try:
            song_uri = None

            if re.match(url_regex, song):
                song_uri = song

            return song, song_uri
        except Exception as e:
            logging.error(f"Song request failed: {e}")
            await ctx.send(f"@{ctx.author.name}, there was an error with your request!")
            return None, None

    @staticmethod
    async def _help(ctx: Context) -> None:
        prefix = get_bot_config().prefix

        await ctx.send(f"{prefix}sr <song name + artist or Spotify URL> - "
                       "Request a song to be added to the queue. "
                       "Example: !sr Never Gonna Give You Up - Rick Astley")

    @staticmethod
    async def blacklist_user(ctx: Context, user: str) -> None:
        if not ctx.author.is_mod:
            return await ctx.send(f"@{ctx.author}You don't have permission to do that.")
        if register_blacklisted_user(user):
            return await ctx.send(f"{user} added to blacklist")
        return await ctx.send(f"{user} is already blacklisted")

    @staticmethod
    async def unblacklist_user(ctx: Context, user: str) -> None:
        if not ctx.author.is_mod:
            return await ctx.send(f"@{ctx.author} you don't have permission to do that.")
        if remove_blacklist_of_user(user):
            return await ctx.send(f"{user} removed from blacklist")
        return await ctx.send(f"{user} is not blacklisted")

    @staticmethod
    async def blacklist_song(ctx: Context, song_uri: str, spotify_instance: Spotify) -> None:
        if not ctx.author.is_mod:
            return await ctx.send("You are not authorized to use this command.")

        if register_blacklisted_song(song_uri):
            track_name = get_track_name_from_uri(spotify_instance, song_uri)
            return await ctx.send(f"{track_name} added to blacklist")
        return await ctx.send("Song is already blacklististed")

    @staticmethod
    async def unblacklist_song(ctx: Context, song_uri: str, spotify_instance: Spotify) -> None:
        if not ctx.author.is_mod:
            return await ctx.send(f"@{ctx.author} you don't have permission to do that.")
        if remove_blacklist_of_song(song_uri):
            track_name = get_track_name_from_uri(spotify_instance, song_uri)
            return await ctx.send(f"{track_name} was removed from the blacklist")
        return await ctx.send("Song is not blacklisted")

    @staticmethod
    async def now_playing(ctx: Context, spotify_instance: Spotify) -> None:
        data = spotify_instance.currently_playing()
        message = get_currently_playing_message(data)
        logging.info(message)
        await ctx.send(message)

    @staticmethod
    async def recently_played(ctx: Context, spotify_instance: Spotify) -> None:
        data = spotify_instance.current_user_recently_played(limit=10)
        message = get_recently_playing_message(data)
        logging.info(message)
        await ctx.send(message)

    @staticmethod
    async def queue(ctx: Context, last_song: str, spotify_instance: Spotify) -> None:
        # todo: maybe @ the person using the command in these messages
        if not last_song:
            await ctx.send("Queue is empty!")
        queue = spotify_instance.queue()
        current_playback = spotify_instance.current_playback()
        message = get_queue_message(queue, current_playback, last_song)
        await ctx.send(message)
