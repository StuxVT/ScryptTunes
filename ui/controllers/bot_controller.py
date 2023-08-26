class BotController:
    def __init__(self, bot_model):
        self.bot_model = bot_model

    def toggle_bot(self):
        self.bot_model.toggle_bot()