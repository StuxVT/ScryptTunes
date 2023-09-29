import logging
import subprocess
import sys
from logging.handlers import RotatingFileHandler


def setup_logging():
    max_log_size = 1 * 1024 * 1024  # 1 MB

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            RichHandler(),
            # RotatingFileHandler("app.log", maxBytes=max_log_size, backupCount=5)  # Rotate after reaching max_log_size
        ]
    )


def main():
    setup_logging()
    logging.info("Application started")

    root = MainApp()
    root.mainloop()


def install_requirements():
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


if __name__ == "__main__":
    # only import deps after insuring installed
    try:
        from rich.logging import RichHandler
        from ui.main_app import MainApp
    except ImportError:
        install_requirements()
        from rich.logging import RichHandler
        from ui.main_app import MainApp

    main()
