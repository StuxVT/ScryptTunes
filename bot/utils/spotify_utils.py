import logging
from typing import Tuple, List
import re


def get_song_details(spotify, song):
    return spotify.search(song, limit=1, type="track", market="US")


def get_album_details(spotify, song_id) -> Tuple[str, List[str], float]:
    """
    Get album name, artist and album duration
    :param spotify: Spotipy Instance
    :param song_id: Song id to find the album of
    :return: album name, artist(s) and album duration in a tuple
    """
    data = spotify.track(song_id)
    song_name = data["name"]
    song_artists = data["artists"]
    song_artists_names = [artist["name"] for artist in song_artists]
    duration = data["duration_ms"] / 60000

    return song_name, song_artists_names, duration


def get_track_name_from_uri(spotify, uri):
    return spotify.track(uri)["name"]


def get_currently_playing_message(data):
    song_artists_names = [artist["name"] for artist in data["item"]["artists"]]

    min_through = int(data["progress_ms"] / (1000 * 60) % 60)
    sec_through = int(data["progress_ms"] / (1000) % 60)
    time_through = f"{min_through} mins, {sec_through} secs"

    min_total = int(data["item"]["duration_ms"] / (1000 * 60) % 60)
    sec_total = int(data["item"]["duration_ms"] / (1000) % 60)
    time_total = f"{min_total} mins, {sec_total} secs"

    return  f"🎶Now Playing - {data['item']['name']} by {', '.join(song_artists_names)} | Link: {data['item']['external_urls']['spotify']} | {time_through} - {time_total}"


def get_recently_playing_message(data):
    songs = []
    for song in data["items"]:
        artists = ", ".join([artist["name"] for artist in song["track"]["artists"]])
        songs.append(f"{song['track']['name']} - {artists}")
    return f"Recently Played: {' | '.join(songs)}"


def get_queue_message(queue, current_playback, last_song):
    # todo: this code looks suprisingly stupid, definitely needs refactoring
    total_songs = 1
    playlist_time_remaining = current_playback['item']['duration_ms'] - current_playback['progress_ms']

    for song in queue['queue'][::-1]:
        last_song_found = False
        if song['id'] == last_song:
            last_song_found = True
        if last_song_found:
            total_songs += 1
            playlist_time_remaining += song['duration_ms']

    total_seconds = playlist_time_remaining // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f'Songs In Queue: {total_songs}| Next added song would play in: {hours} hours {minutes:02}:{seconds:02} minutes'