import logging
import sys
from rich.logging import RichHandler
from pathlib import Path
import dotenv
from bot.scrypt_tunes import Bot\

# todo: config check
'''
     init .env, blacklist, blacklist_user, and config.json if they dont exist
     
     for file in config/default
         ensure file exists in config/
            if missing create file
            ensure all keys in file exist in matching config/* file
                if missing ask for it
'''

log_level = logging.DEBUG if "dev".lower() in sys.argv else logging.INFO

log = logging.getLogger()
logging.basicConfig(
    level=log_level,
    format="%(name)s - %(message)s",
    datefmt="%X",
    handlers=[RichHandler()],
)

cwd = Path(__file__).parents[0]
cwd = str(cwd)

dotenv.load_dotenv("config/.env")

if __name__ == "__main__":
    bot = Bot()
    bot.run()