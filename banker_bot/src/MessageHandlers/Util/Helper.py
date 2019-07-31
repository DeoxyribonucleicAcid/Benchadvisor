import os
import sys

from banker_bot.src.State import State


def build_msg_restart(bot, update):
    if State.DEBUG:
        bot.send_message(chat_id=update.message.chat_id, text='bot restarted')
        os.execl(sys.executable, sys.executable, *sys.argv)


def test(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='bot responds')
    return None



def reset_states(bot, chat_id: int):
    #DBAccessor.update_player(_id=chat_id,
    #                         update=DBAccessor.get_update_query_player(nc_msg_state=Constants.NC_MSG_States.INFO))
    bot.send_message(chat_id=chat_id, text='To be implemented.\nStates have not been reset')


def shorten_logfile():
    #TODO
    return None