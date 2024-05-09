from customtkinter import CTkFrame, CTkLabel, CTkEntry

from ui.frames.list_input import ListInput


# TODO: the only making this different from text_setting_row is the nested list setting, these need parent
class ListSettingRow(CTkFrame):
    def __init__(
        self, parent, setting_name: str, setting_description: str, initial_value: list
    ):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        label_frame = CTkFrame(self)
        label_frame.grid(row=0, column=0, sticky="ew")

        self.name_label = CTkLabel(
            label_frame, text=setting_name, font=("Roboto", 14, "bold")
        )
        self.name_label.pack(side="top", fill="both", expand=True)

        self.description_label = CTkLabel(
            label_frame, text=setting_description, font=("Roboto", 12)
        )
        self.description_label.pack(side="top", fill="both", expand=True)

        widget_frame = CTkFrame(self)
        widget_frame.grid(row=0, column=1, sticky="ew")

        self.list_setting = ListInput(widget_frame, initial_value)
        self.list_setting.pack()

    def get(self):
        return self.list_setting.get()
