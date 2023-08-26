
from ui.frames.main_frame import MainFrame
from ui.frames.sidebar import Sidebar


class MainView:
    def __init__(self, root, bot_controller, settings_controller):
        self.main_frame = MainFrame(root, bot_controller, settings_controller)
        self.sidebar = Sidebar(root, bot_controller, settings_controller, title="ScryptTunes")

    def show(self):
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

