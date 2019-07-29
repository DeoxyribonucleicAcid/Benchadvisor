from MessageHandlers import NewBenchHandler


class CALLBACK_HANDLER:
    callbacks = {
        'menu': {
            'new': NewBenchHandler.handle_new_bench,
        }
    }

    @staticmethod
    def handle(bot, update):
        elems = update.callback_query.data.split('%')
        id_elems = elems[0].split('-')
        params = elems[1:]
        cb_function = CALLBACK_HANDLER.callbacks[id_elems[0]]
        for id in id_elems[1:]:
            cb_function = cb_function[id]
        if type(cb_function) is type(None):
            return bot.send_message(chat_id=update.effective_message.chat_id,
                                    text='Method not implemented :/')
        return cb_function(bot, update, *params)


def process_callback(bot, update):
    CALLBACK_HANDLER.handle(bot=bot, update=update)
