import logging
from logging.handlers import RotatingFileHandler  # Import RotatingFileHandler
from rich.logging import RichHandler
from ui.main_app import MainApp


def setup_logging():
    max_log_size = 1 * 1024 * 1024  # 1 MB

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            RichHandler(),
            RotatingFileHandler("app.log", maxBytes=max_log_size, backupCount=5)  # Rotate after reaching max_log_size
        ]
    )


def main():
    setup_logging()
    logging.info("Application started")

    root = MainApp()
    root.mainloop()


if __name__ == "__main__":
    main()
