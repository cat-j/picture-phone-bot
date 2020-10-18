from telegram.ext import (
    CommandHandler,
    Updater
)

class Bot:

    def __init__(self):
        self.token = self.get_token()
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def get_token(self):
        with open("./token", 'r') as f:
            return f.read()

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="dutch apple ass")

    def newgame(self, update, context):
        if update.message.chat.type == 'group':
            context.bot.send_message(chat_id=update.effective_chat.id, text="dutch apple ass")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="you're not in a group")

    def _register_commands(self):
        handlers = [
            CommandHandler('start', self.start),
            CommandHandler('newgame', self.newgame)
            ]

        for handler in handlers:
            self.dispatcher.add_handler(handler)

    def run(self):
        self._register_commands()
        self.updater.start_polling()

raul = Bot()
raul.run()