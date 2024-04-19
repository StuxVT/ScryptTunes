import os
from enum import Enum

SCRYPTTUNES_DATA = os.path.join(os.getenv('LOCALAPPDATA'), "Stux\\ScryptTunes\\")
SCRYPTTUNES_DATA_CONFIG = os.path.join(os.getenv('LOCALAPPDATA'), "Stux\\ScryptTunes\\config")


SONG_BLACKLIST = os.path.join(SCRYPTTUNES_DATA_CONFIG, "blacklist.json")
USER_BLACKLIST = os.path.join(SCRYPTTUNES_DATA_CONFIG, "blacklist_user.json")
CONFIG = os.path.join(SCRYPTTUNES_DATA_CONFIG, "config.json")
CACHE = os.path.join(SCRYPTTUNES_DATA_CONFIG, ".cache")


class Permission(Enum):
    SUBBED = 'subscriber'
    SUB_GIFTER = 'sub-gifter'
    VIP = 'vip'
    MOD = 'moderator'
    BROADCASTER = 'broadcaster'

