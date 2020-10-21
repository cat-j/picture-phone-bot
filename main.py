import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
    )
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Updater
    )
from bot_runner import BotRunner

runner = BotRunner()
runner.run_bot()