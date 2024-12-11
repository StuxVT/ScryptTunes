import logging
import os
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler
from tkinter import WORD, END
from customtkinter import CTkFrame, CTkTabview, CTkTextbox

from constants import SCRYPTTUNES_DATA_CONFIG

class MainFrame(CTkFrame):
    def __init__(self, master, bot_controller, settings_controller):
        super().__init__(master, corner_radius=0, fg_color="transparent")

        self.bot_controller = bot_controller
        self.settings_controller = settings_controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create tabview
        self.tabview = CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.tabview.add("Log")

        self.log_text = CTkTextbox(master=self.tabview.tab("Log"), wrap=WORD)
        self.log_text.pack(side="top", fill="both", expand=True)

        # Configure logging
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        gui_handler = CTkTabviewHandler(self.log_text)
        gui_handler.setLevel(logging.INFO)
        logger.addHandler(gui_handler)
    
        log_file_path = os.path.join(SCRYPTTUNES_DATA_CONFIG, "app.log")
        file_handler = RotatingFileHandler(
            log_file_path, mode='a', maxBytes=1*1024*1024, backupCount=1, encoding="utf-8", delay=0
        )
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

class CTkTabviewHandler(RichHandler):
    def __init__(self, text_widget: CTkTextbox):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record: logging.LogRecord):
        try:
            log_message = self.format(record)
            # Send the log message to the Text widget
            self.text_widget.insert(END, log_message + "\n")
            # Automatically scroll to the end to show the latest log message
            self.text_widget.see(END)
        except Exception as e:
            print(f"Error emitting log message: {e}")