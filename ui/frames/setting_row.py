from customtkinter import CTkFrame, CTkLabel


class SettingRow(CTkFrame):
    def __init__(self, parent, setting_name, setting_description, input_widget):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        self.name_label = CTkLabel(self, text=setting_name, font=("Roboto", 14, "bold"))
        self.name_label.grid(row=0, column=0, sticky="ew")

        self.description_label = CTkLabel(self, text=setting_description, font=("Roboto", 12))
        self.description_label.grid(row=1, column=0, sticky="ew")

        self.input_widget = input_widget
        self.input_widget.grid(row=0, column=1, rowspan=2, padx=10, sticky="ew")

    def get_setting_value(self):
        return self.input_widget

