from handlers.handler_com import HandlerCommand
from handlers.handler_all_text import HandlerAllText
from handlers.handler_inline_query import HandlerInlineQuery


class HandlerMain:
    """
    Класс компоновщик
    """
    def __init__(self, bot):
        self.bot = bot
        self.handler_commands = HandlerCommand(self.bot)
        self.handler_all_text = HandlerAllText(self.bot)
        self.handler_inline_query = HandlerInlineQuery(self.bot)

    def handle(self):
        self.handler_commands.handle()
        self.handler_all_text.handle()
        self.handler_inline_query.handle()
