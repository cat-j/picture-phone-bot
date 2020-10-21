import logging

from picture_phone_game import (
    PicturePhoneGame
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Updater
)


JOIN_GAME = "join"


class GameDatabase:

    def __init__(self, debug=False):
        self.contents = {}
        self.debug = debug

    def add_new_game(self, new_game_id):
        self.contents[new_game_id] = PicturePhoneGame(self.debug)

    def get_game(self, game_id):
        return self.contents[game_id]


class BotTexts:

    def __init__(self):
        self.start = "dutch apple ass"
        self.newgame_group = "dutch apple ass"
        self.newgame_other = "you're not in a group"


class BotRunner:

    def __init__(self):
        self.token = self._token()
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.games = GameDatabase()
        self.texts = BotTexts()

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    ### PUBLIC ###

    def start(self, chat_update, context):
        self._reply_text(chat_update, context, self.texts.start)

    def newgame(self, chat_update, context):
        if chat_update.message.chat.type == 'group':
            self._reply_join_button(chat_update)
            self._create_game_for_group(chat_update)
        else:
            self._reply_not_in_group(chat_update, context)

    def run_bot(self):
        self._register_handlers()
        self.updater.start_polling()

    ### PRIVATE ###

    def _create_game_for_group(self, group_update):
        group_chat_id = self._chat_id_from_update(group_update)
        self.games.add_new_game(group_chat_id)

    def _handle_button_press(self, button_press_update, context):
        user_action = self._callback_query_data(button_press_update)
        if user_action == JOIN_GAME:
            self._join_user_who_pressed(button_press_update, context)

    def _join_user_who_pressed(self, button_press_update, context):
        joining_user_id = self._sender_user_id(button_press_update)
        game_id = self._chat_id_from_update(button_press_update.callback_query)
        game = self.games.get_game(game_id)
        game.join_player(joining_user_id)

        context.bot.send_message(chat_id=joining_user_id, text="boston cream splat")

    def _reply_join_button(self, chat_update_to_reply_to):
        chat_update_to_reply_to.message.reply_text(
            text=self.texts.newgame_group,
            reply_markup=self._join_button(),
            quote=False
        )

    def _chat_id_from_update(self, chat_update):
        return chat_update.message.chat.id

    def _reply_not_in_group(self, chat_update_to_reply_to, context):
        self._reply_text(chat_update_to_reply_to, context, self.texts.newgame_other)

    def _callback_query_data(self, button_press_update):
        return button_press_update.callback_query.data

    def _sender_user_id(self, update):
        return update.effective_user.id

    def _register_handlers(self):
        handlers = [
            CommandHandler('start', self.start),
            CommandHandler('newgame', self.newgame),
            CallbackQueryHandler(self._handle_button_press)
        ]

        for handler in handlers:
            self.dispatcher.add_handler(handler)

    def _reply_text(self, update, context, text_to_send):
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_send)

    def _token(self):
        with open("./token", 'r') as f:
            return f.read()

    def _join_button(self):
        button = InlineKeyboardButton(
                text="Join",
                callback_data=JOIN_GAME
                )
        return InlineKeyboardMarkup([[button]])