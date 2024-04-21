from customtkinter import CTkFrame, CTkLabel, CTkCheckBox, IntVar

from ui.models.config import PermissionSetting, PermissionConfig


class PermissionSettingRow(CTkFrame):
    def __init__(self, parent, setting_name, setting_description, initial_values, command_name):
        super().__init__(parent)

        self.command_name = command_name

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

        # Unsubbed Setting
        self.unsubbed_value = IntVar(value=initial_values)
        self.unsubbed_checkbox = CTkCheckBox(
            widget_frame, variable=self.unsubbed_value, onvalue=1, offvalue=0, text="Unsubbed"
        )
        self.unsubbed_checkbox.pack()

        # subbed Setting
        self.subbed_value = IntVar(value=initial_values)
        self.subbed_checkbox = CTkCheckBox(
            widget_frame, variable=self.subbed_value, onvalue=1, offvalue=0, text="Subbed"
        )
        self.subbed_checkbox.pack()

        # sub_gifter Setting
        self.sub_gifter_value = IntVar(value=initial_values)
        self.sub_gifter_checkbox = CTkCheckBox(
            widget_frame, variable=self.sub_gifter_value, onvalue=1, offvalue=0, text="Subbed"
        )
        self.sub_gifter_checkbox.pack()

        # VIP Setting
        self.vip_value = IntVar(value=initial_values)
        self.vip_checkbox = CTkCheckBox(
            widget_frame, variable=self.vip_value, onvalue=1, offvalue=0, text="VIP"
        )
        self.vip_checkbox.pack()

        # Mod Setting
        self.mod_value = IntVar(value=initial_values)
        self.mod_checkbox = CTkCheckBox(
            widget_frame, variable=self.mod_value, onvalue=1, offvalue=0, text="Mod"
        )
        self.mod_checkbox.pack()

        # Streamer Setting
        self.streamer_value = IntVar(value=initial_values)
        self.streamer_checkbox = CTkCheckBox(
            widget_frame, variable=self.streamer_value, onvalue=1, offvalue=0, text="Streamer"
        )
        self.streamer_checkbox.pack()

    def get(self):
        return PermissionSetting(
            command_name=self.command_name,
            permission_config=PermissionConfig(
                unsubbed=bool(self.unsubbed_value.get()),
                subbed=bool(self.subbed_value.get()),
                sub_gifter=bool(self.sub_gifter_value.get()),
                vip=bool(self.vip_value.get()),
                mod=bool(self.mod_value.get()),
                streamer=bool(self.streamer_value.get())
            )
        )
