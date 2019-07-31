import logging

import setup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from src.State import State

from MessageHandlers.Util import Actions, Helper
from MessageHandlers import ReplyCallbackHandler, NewBenchHandler, MenuMessageBuilder, HelpMessageBuilder, StartHandler


# TODO-List:
#   items
#   use items
#   trade pokemon
#   duels
#   inspect pokemon
#   train pokemon
#   config/game menu - wip
#   Tests
#   German
#   use tempfile

@Actions.send_typing_action
def command_handler_start(bot, update):
    StartHandler.build_msg_start(bot=bot, update=update)


@Actions.send_typing_action
def command_handler_new_bench(bot, update):
    NewBenchHandler.handle_new_bench(bot=bot, update=update)


@Actions.send_typing_action
def command_handler_help(bot, update):
    HelpMessageBuilder.build_msg_help(bot=bot, update=update)


def command_handler_menu(bot, update):
    MenuMessageBuilder.send_menu_message(bot=bot, update=update)


def callback_handler(bot, update):
    ReplyCallbackHandler.process_callback(bot=bot, update=update)


# Keepalive
def logfile_handler(bot, job):
    Helper.shorten_logfile()


# DEBUG
def command_handler_restart(bot, update):
    Helper.build_msg_restart(bot=bot, update=update)


def command_handler_test(bot, update, args):
    Helper.test(bot, update)


def command_handler_reset(bot, update):
    Helper.reset_states(bot, update.message.chat_id)


def main():
    logging.basicConfig(filename='.log', level=logging.DEBUG, filemode='w')
    setup.prepare_environment()

    updater = Updater(token=State.token, request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', callback=command_handler_start)
    newBench_handler = CommandHandler('new', callback=command_handler_new_bench)
    # DEBUG
    restart_handler = CommandHandler('restart', callback=command_handler_restart)
    test_handler = CommandHandler('test', callback=command_handler_test, pass_args=True)
    callback_query_handler = CallbackQueryHandler(callback=callback_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(newBench_handler)
    # DEBUG
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(test_handler)
    #
    dispatcher.add_handler(callback_query_handler)

    updater.start_polling()
    j = updater.job_queue
    j.run_repeating(logfile_handler, interval=60 * 15, first=0)


main()
