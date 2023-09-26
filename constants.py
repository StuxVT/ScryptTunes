import os

SCRYPTTUNES_DATA = os.path.join(os.getenv('LOCALAPPDATA'), "Stux/ScryptTunes/")
SCRYPTTUNES_DATA_CONFIG = os.path.join(os.getenv('LOCALAPPDATA'), "Stux/ScryptTunes/config")
SCRYPTTUNES_DATA_CONFIG_DEFAULT = os.path.join(os.getenv('LOCALAPPDATA'), "Stux/ScryptTunes/config/default")

# Configs
DEFAULT_BLACKLIST_PATH = os.path.join(SCRYPTTUNES_DATA, "config/default/blacklist.json")
DEFAULT_USER_BLACKLIST_PATH = os.path.join(SCRYPTTUNES_DATA, "config/default/blacklist_user.json")

SONG_BLACKLIST_PATH = os.path.join(SCRYPTTUNES_DATA, "config/blacklist.json")
USER_BLACKLIST_PATH = os.path.join(SCRYPTTUNES_DATA, "config/blacklist_user.json")


