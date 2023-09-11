import tkinter as tk
from customtkinter import CTkFrame, CTkButton, CTkEntry

from ui.components.custom_listbox import CustomListbox


# (thanks chatgpt)
class ListInput(CTkFrame):
    def __init__(self, master, items=None):
        super().__init__(master)
        self.item_list = items if items is not None else []  # List to store items

        self.item_entry = CTkEntry(self)
        self.add_button = CTkButton(self, text="Add Item", command=self.add_item)
        self.remove_button = CTkButton(self, text="Remove Selected Item", command=self.remove_selected_item)

        self.listbox = CustomListbox(self, selectmode=tk.SINGLE)
        for item in self.item_list:
            self.listbox.insert(tk.END, item)

        self.item_entry.pack()
        self.add_button.pack()
        self.remove_button.pack()
        self.listbox.pack()

    def add_item(self):
        item = self.item_entry.get()
        if item:
            self.item_list.append(item)
            self.listbox.insert(tk.END, item)
            self.item_entry.delete(0, tk.END)

    def remove_selected_item(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            item_index = selected_index[0]
            removed_item = self.listbox.get(item_index)
            self.listbox.delete(item_index)
            self.item_list.remove(removed_item)

    def get(self):
        return self.item_list
