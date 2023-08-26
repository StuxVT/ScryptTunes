from customtkinter import CTkFrame, CTkButton

class HomeFrame(CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.home_button = CTkButton(self, text="Home Button")
        self.home_button.pack(padx=20, pady=20)
