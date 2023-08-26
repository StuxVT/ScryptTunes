import logging
from logging.handlers import RotatingFileHandler  # Import RotatingFileHandler
from rich.logging import RichHandler
import customtkinter as ctk
from gui.main_app import MainApp

def setup_logging():
    max_log_size = 1 * 1024 * 1024  # 1 MB

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            RichHandler(),
            RotatingFileHandler("app.log", maxBytes=max_log_size, backupCount=5)  # Rotate after reaching max_log_size
        ]
    )

def main():
    setup_logging()
    logging.info("Application started")

    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
