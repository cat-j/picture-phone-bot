from telegram.ext import (
    CommandHandler,
    Updater
)

class BotTexts:

    def __init__(self):
        self.start = "dutch apple ass"
        self.newgame_group = "dutch apple ass"
        self.newgame_other = "you're not in a group"


class BotRunner:

    def __init__(self):
        self.token = self._get_token()
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.texts = BotTexts()

    # PUBLIC

    def start(self, update, context):
        self._reply_text(update, context, self.texts.start)

    def newgame(self, update, context):
        if update.message.chat.type == 'group':
            group = update.message.chat
            print(group)
            print(type(group))
            self._reply_text(update, context, self.texts.newgame_group)
        else:
            self._reply_text(update, context, self.texts.newgame_other)

    def run(self):
        self._register_commands()
        self.updater.start_polling()

    # PRIVATE

    def _register_commands(self):
        handlers = [
            CommandHandler('start', self.start),
            CommandHandler('newgame', self.newgame)
            ]

        for handler in handlers:
            self.dispatcher.add_handler(handler)

    def _reply_text(self, update, context, text_to_send):
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_send)

    def _get_token(self):
        with open("./token", 'r') as f:
            return f.read()


raul = BotRunner()
raul.run()