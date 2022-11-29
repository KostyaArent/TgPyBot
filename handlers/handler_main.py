from handlers.handler_com import HandlerCommand


class HandlerMain:
    """
    Класс компоновщик
    """
    def __init__(self, bot):
        self.bot = bot
        self.handler_commands = HandlerCommand(self.bot)

    def handle(self):
        self.handler_commands.handle()