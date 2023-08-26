class BotModel:
    def __init__(self):
        self.bot_enabled = False

    def toggle_bot(self):
        self.bot_enabled = not self.bot_enabled
