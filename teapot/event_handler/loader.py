from discord.ext import commands
import importlib
import os

class EventHandlerLoader:
    """
    Dynamically loads event handler modules and registers a unified on_message event.

    As discord only allows one on_message event, this loader collects all on_message handlers
    from the event_handler submodules and calls them sequentially.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.handlers = []
        self.load_event_handlers()
        self.register_on_message()

    def load_event_handlers(self):
        """
        Scan for all python file in the event_handler directory to find on_message handlers.
        """
        handler_dir = os.path.dirname(__file__)
        for fname in os.listdir(handler_dir):
            if fname.endswith('.py') and fname not in ('__init__.py', 'loader.py'):
                mod_name = f'teapot.event_handler.{fname[:-3]}'
                module = importlib.import_module(mod_name)
                if hasattr(module, 'on_message_handler'):
                    self.handlers.append(module.on_message_handler)
    
    def get_registered_handlers(self):
        return self.handlers

    def register_on_message(self):
        @self.bot.event
        async def on_message(message):
            for handler in self.handlers:
                await handler(self.bot, message)
            await self.bot.process_commands(message)