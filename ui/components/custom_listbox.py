"""
theme data for ctkentry

  "CTkEntry": {
    "corner_radius": 6,
    "border_width": 2,
    "fg_color": ["#F9F9FA", "#343638"],
    "border_color": ["#979DA2", "#565B5E"],
    "text_color":["gray10", "#DCE4EE"],
    "placeholder_text_color": ["gray52", "gray62"]
  }
"""
from tkinter import Listbox, SINGLE


class CustomListbox(Listbox):
    def __init__(self, master, selectmode=SINGLE):
        super().__init__(
            master,
            borderwidth=2,
            fg="#F9F9FA",
            bg="#343638",
            selectmode=selectmode
        )
