import os

nuitka_binary_dir = os.path.dirname(__file__)

# Configs
SONG_BLACKLIST = os.path.join(nuitka_binary_dir, "blacklist.dat")
USER_BLACKLIST = os.path.join(nuitka_binary_dir, "blacklist_user.dat")
CONFIG = os.path.join(nuitka_binary_dir, 'config.dat')


