from pydantic import BaseModel


class SettingsModel(BaseModel):
    nickname: str = ""
    prefix: str = "!"
    channels: list = [""]
    token: str = ""
    client_id: str = ""
    client_secret: str = ""
    channel_points_reward: str = ""
    spotify_client_id: str = ""
    spotify_secret: str = ""
    spotify_redirect_uri: str = ""
