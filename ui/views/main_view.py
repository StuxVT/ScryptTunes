from ui.frames.main_frame import MainFrame


class MainView:
    def __init__(self, root, bot_controller, settings_controller):
        self.main_frame = MainFrame(root, bot_controller, settings_controller)

    def show(self):
        self.main_frame.pack()
