from pydantic import BaseModel


class Config(BaseModel):
    nickname: str = ""
    prefix: str = "!"
    channel: str = ""
    token: str = ""
    client_id: str = ""
    client_secret: str = ""
    channel_points_reward: str = ""
    spotify_client_id: str = ""
    spotify_secret: str = ""
    spotify_redirect_uri: str = ""
    spotify_playlist_href: str = ""
