from typing import List

from pydantic import BaseModel


class PermissionConfig(BaseModel):
    unsubbed: bool = False
    subscriber: bool = False
    vip: bool = False
    mod: bool = False
    broadcaster: bool = False


class PermissionSetting(BaseModel):
    command_name: str
    permission_config: PermissionConfig


class PermissionSettingDict(BaseModel):
    ping_command: PermissionSetting


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
    rate_limit: int = 0
    permissions: PermissionSettingDict  # todo: dynamically build dict based on PermissionSetting data
