import Constants
import telegram
from Entities.Bench import Bench
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Endpoints import DBEndpoint as Endpoint


def handle_new_bench(bot, update):
    bench = Bench()
    reply_markup = get_star_keyboard(bench.bench_id)

    msg = bot.send_message(chat_id=update.message.chat_id,
                           text='0 Ratings | average: ',
                           reply_markup=reply_markup)
    bench.message_id = msg.message_id
    Endpoint.insert_new_bench(bench=bench)


def handle_rating(bot, update, bench_id, rating):
    bench = Endpoint.get_bench(bench_id)
    if bench is None:
        raise ValueError('Bench with bench_id ' + str(bench_id) + ' was not found')
    name  = update.callback_query.from_user.username if update.callback_query.from_user.username is not None else update.callback_query.from_user.first_name
    user_in_ratings = [(i, x) for i, x in enumerate(bench.ratings) if x.user_id == str(update.callback_query.from_user.id)]
    if user_in_ratings is None or len(user_in_ratings) == 0:
        bench.ratings.append(Bench.Rating(user_id=update.callback_query.from_user.id,
                                          username=name,
                                          rating=float(rating)))
    else:
        bench.ratings[user_in_ratings[0][0]].rating = float(rating)
    query = {'$set': {'ratings': [{'rating_id': str(i.rating_id),
                                   'user_id': str(i.user_id),
                                   'username': str(i.username),
                                   'rating': float(i.rating),
                                   } for i in bench.ratings] if bench.ratings is not None else None}}
    Endpoint.update_bench(bench_id, query)
    av_rating = sum(bench.ratings) / len(bench.ratings)
    text = '{} Ratings | average: {}'.format(len(bench.ratings), av_rating)
    for i in bench.ratings:
        text += '\n{} rated: {}'.format(i.username, i.rating)
    reply_markup = get_star_keyboard(bench.bench_id)
    try:
        bot.edit_message_text(chat_id=update.effective_chat.id, text=text, message_id=bench.message_id,
                              reply_markup=reply_markup)
    except telegram.error.BadRequest as e:
        if e.message != 'Message is not modified':
            raise e


def get_star_keyboard(bench_id):
    keys = [[], []]
    # stars = ''
    for i in range(10):
        # if i % 2 == 1:
        #    stars += u"\u2605"
        # halfstar = u"\u2BEA" if i % 2 == 0 else ''
        keys[int(i / 5)].append(InlineKeyboardButton(text=str((i + 1) / 2) + u"\u2605",
                                                     callback_data=Constants.CALLBACK.BENCH_RATING(bench_id,
                                                                                                   (i + 1) / 2)))
    return InlineKeyboardMarkup(inline_keyboard=keys)
