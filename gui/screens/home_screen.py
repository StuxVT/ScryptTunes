from customtkinter import CTk
from gui.frames.home_frame import HomeFrame

class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Screen")

        self.home_frame = HomeFrame(self.root)

        self.home_frame.pack(fill="both", expand=True)
        self.setup_widgets()

    def setup_widgets(self):
        self.home_frame.home_button.configure(command=self.handle_home_button_click)

    def handle_home_button_click(self):
        print("Home button clicked!")

    def hide(self):
        self.home_frame.pack_forget()

    def show(self):
        self.home_frame.pack(fill="both", expand=True)
