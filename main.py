import ctypes
import logging
from rich.logging import RichHandler
from ui.main_app import MainApp
import os
from logging.handlers import RotatingFileHandler

import constants


def setup_logging():
    max_log_size = 1 * 1024 * 1024  # 1 MB

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            RichHandler(),
            RotatingFileHandler(os.path.join(constants.SCRYPTTUNES_DATA, "app.log"), maxBytes=max_log_size, backupCount=5)  # Rotate after reaching max_log_size
        ]
    )


def main():
    setup_logging()
    logging.info("Application started")

    root = MainApp()
    root.title("ScryptTunes")
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('ai.stux.scrypttunes')
    root.iconbitmap('icon.ico')
    root.mainloop()


if __name__ == "__main__":
    os.makedirs(constants.SCRYPTTUNES_DATA, exist_ok=True)
    os.makedirs(constants.SCRYPTTUNES_DATA_CONFIG, exist_ok=True)
    main()
