from customtkinter import CTkFrame, CTkLabel, CTkCheckBox, IntVar


class CheckboxSettingRow(CTkFrame):
    def __init__(self, parent, setting_name, setting_description, initial_value):
        super().__init__(parent)
        self.columnconfigure(0, minsize=300)  # todo: dynamic adjustment somehow based on context?
        self.columnconfigure(1, weight=2)

        label_frame = CTkFrame(self)
        label_frame.grid(row=0, column=0, sticky="ew")

        self.name_label = CTkLabel(label_frame, text=setting_name, font=("Roboto", 14, "bold"))
        self.name_label.pack(side="top", fill="both", expand=True)

        self.description_label = CTkLabel(label_frame, text=setting_description, font=("Roboto", 12))
        self.description_label.pack(side="top", fill="both", expand=True)

        widget_frame = CTkFrame(self)
        widget_frame.grid(row=0, column=1, sticky="ew")
        self.value = IntVar(value=initial_value)
        self.check_setting = CTkCheckBox(widget_frame, variable=self.value, onvalue=1, offvalue=0)
        self.check_setting.pack()

    def get(self):
        return self.check_setting.get()
