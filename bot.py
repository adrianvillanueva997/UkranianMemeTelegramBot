import logging
import random

import telegram.chataction
from telegram.ext import Updater, CommandHandler, run_async, CallbackQueryHandler

import src.Artifact
import src.Dota
import src.RPG
import src.config as config
import src.eight_chan
import src.four_chan
import src.google_scrapping
import src.online_apis
import src.wikired

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_args_as_string(args):
    string = ''
    for arg in args:
        string += arg + ' '
    return string


def start(update, context):
    update.message.reply_text('Pues estoy funcionando')


def help(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    update.message.reply_text(text="Sigo vivo")


def donate(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    update.message.reply_text(text='paypal.me/thexiao77')


def error(update, context, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


@run_async
def joke(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        text = handler.joke()
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=text)
    except Exception as e:
        print(e)


@run_async
def get_time_zone(update, context):
    try:
        # bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        data = handler.get_time_zone(context.args[0])
        message = ('Location: ' + data['location'] +
                   '\nHour: ' + data['hour'] +
                   '\nZone Name: ' + data['zone_name'] +
                   '\nTime Zone: ' + data['time_zone'])
        context.bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Location not found')


@run_async
def send_location(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        # print(context.args[0])
        # handler = src.online_apis.OnlineApis()
        # geodata = handler.get_coords(context.args[0])
        # print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))

        # context.bot.send_message(chat_id=update.message.chat_id,
        #                        text='{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
        # context.bot.sendLocation(chat_id=update.message.chat_id, latitude=geodata['lat'], longitude=geodata['lng'])
        context.bot.send_message(chat_id=update.message.chat_id,
        #                         text='Aun no funciono')

    except Exception as exception:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Location not found')
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)


def send_wikipedia(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        args = get_args_as_string(context.args)
        article = handler.send_wikipedia(args)
        context.bot.send_message(chat_id=update.message.chat_id, text=article.url)
    except Exception as exception:
        print(exception)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Search not found')
        logger.warning('Update "%s" caused error "%s"' % (update, error))


def check4_chan_board(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.four_chan.FourChanHandler()
        message = handler.check4_chan_board(context.args[0])
        update.send_message(chat_id=update.message.chat_id,
                            text=message)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='board not found')


@run_async
def random_board(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.four_chan.FourChanHandler()
        message, url = handler.random_board()
        print(message, url)
        if '.webm' not in url:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=url)
            context.bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=url)
            context.bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='board not found')


@run_async
def weather(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        args = get_args_as_string(context.args)
        data = handler.weather(args)
        print(data)
        message = f'Location: {args} \n' \
                  f'Humidity: {data["humidity"]}% \n' \
                  f'Temperature (max): {data["temperature"]["temp_max"]} ºC \n' \
                  f'Temperature (now): {data["temperature"]["temp"]} ºC \n' \
                  f'Temperature (min): {data["temperature"]["temp_min"]} ºC \n' \
                  f'Wind: {data["wind"]["speed"]} m/s \n' \
                  f'Clouds: {data["clouds"]} % \n' \
                  f'Pressure: {data["pressure"]["press"]} hPa'
        update.message.reply_text(message)
    except Exception as error:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(error))


def wiki_red(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.wikired.Wikired()
        tweet = handler.wiki_red()
        context.bot.send_message(chat_id=update.message.chat_id, text=tweet)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        update.message.reply_text(text=str('Try again later'))


def wikibab(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.wikired.Wikired()
        tweet = handler.wiki_bab()
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=tweet)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str('Try again later'))


@run_async
def random_8chan_booard(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.eight_chan.EightChanHandler()
        message, url = handler.random_8_chan_board()
        print(message, url)
        if '.webm' not in url:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=url)
            context.bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=url)
            context.bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=('board not found'))


@run_async
def random8_chan_thread(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.eight_chan.EightChanHandler()
        message, url = handler.random8_chan_thread(context.args[0])
        print(message, url)
        if '.webm' not in url:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=url)
            context.bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=url)
            context.bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=('board not found'))


def list_8_chan_boards(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.eight_chan.EightChanHandler()
        boards = handler.list_8_chan_boards()
        context.bot.send_message(chat_id=update.message.chat_id, text=boards)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=('board not found'))


def list4_chan_boards(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.four_chan.FourChanHandler()
        boards = handler.list_4_chan_boards()
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=boards)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))


@run_async
def search_image(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        args = get_args_as_string(context.args)
        handler = src.google_scrapping.GoogleScrapper(args)
        picture = handler.search_image()
        update.message.reply_text(picture)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))


@run_async
def get_pro_dota_games(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        games = src.Dota.get_pro_dota_games()
        for game in games:
            context.bot.send_message(chat_id=update.message.chat_id, text=game)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))


@run_async
def simpsons_quote(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        picture, quotes = handler.simpsons_quote()
        context.bot.send_photo(chat_id=update.message.chat_id, photo=picture, caption=quotes)

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))


def roll_the_dice(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        number = src.RPG.roll_the_dice(context.args[0])
        update.message.reply_text(number)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))


@run_async
def random_thread(update, context):
    try:
        handler = src.four_chan.FourChanHandler()
        boards = handler.boards

        i = 0
        j = 0
        keyboard = []
        array_list = []
        while i < len(boards):
            if j < 8:
                array_list.append(telegram.InlineKeyboardButton(boards[i], callback_data=boards[i]))
                j += 1
                i += 1
            else:
                temp_list = array_list
                keyboard.append(temp_list[:])
                j = 0
                array_list.clear()
                temp_list.clear()

        # 'w', 'wsg', 'wsr', 'x', 'y'
        outside_boards = [telegram.InlineKeyboardButton("w", callback_data='w'),
                          telegram.InlineKeyboardButton("wsg", callback_data='wsg'),
                          telegram.InlineKeyboardButton("wsr", callback_data='wsr'),
                          telegram.InlineKeyboardButton("x", callback_data='x'),
                          telegram.InlineKeyboardButton("y", callback_data='y'), ]

        keyboard.append(outside_boards[:])
        reply_markup = telegram.InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str('Try again later'))


def chan_4_button(update, context):
    try:

        query = update.callback_query
        print(query)
        print(query.data)
        handler = src.four_chan.FourChanHandler()
        message, url = handler.random_thread(query.data)
        context.bot.edit_message_text(text="Selected option: {}".format(query.data) + '\n' + url + '\n' + message,
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id)
        return query.data

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str('Try again later'))


def kalash_traidor(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        frases_kalash = ['U L T R A I C I O N A D O']
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=frases_kalash[random.randint(0, len(frases_kalash) - 1)])
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str('Try again later'))


def wikired_speech(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.wikired.Wikired()
        tweet = handler.text_to_speech()
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=tweet)
        context.bot.send_audio(chat_id=update.message.chat_id,
                               audio=open('ukranian_audio.mp3', 'rb'))

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str('Try again later'))


def ukrania_today(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.wikired.Wikired()
        tweet = handler.ukrania_today()
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=tweet)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str('Try again later'))


def ukranian(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.wikired.Wikired()
        tweet = handler.ukranian()
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=tweet)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str('Try again later'))


def get_dota_procircuit(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        tournaments = src.Dota.get_dota_procircuit()

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=tournaments)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str('Try again later'))


def text_speech(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.RECORD_AUDIO)
        handler = src.wikired.Wikired()
        args = get_args_as_string(context.args)
        file = handler.tts(args)
        context.bot.send_voice(chat_id=update.message.chat_id, voice=open('ukranian_audio.mp3', 'rb'))

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str('Try again later'))


def call(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.RECORD_AUDIO)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='@DarkTrainer, @Dvdgg, @LilNarwhal, @thexiao77 D O T A')
        urls = []
        with open('src/images/image_urls.txt', 'r', encoding='utf-8') as file:
            for data in file:
                urls.append(data)
        rand = random.randint(0, len(urls))
        context.bot.send_photo(chat_id=update.message.chat_id, photo=urls[rand])
    except Exception as e:
        print(e)


def main():
    updater = Updater(config.updater, workers=4, use_context=True)
    dp = updater.dispatcher
    start_handler = CommandHandler('start', start)

    dp.add_handler(start_handler)
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("locate", send_location, pass_args=True))
    dp.add_handler(CommandHandler("wikipedia", send_wikipedia, pass_args=True))
    dp.add_handler(CommandHandler("board", check4_chan_board, pass_args=True))
    dp.add_handler(CommandHandler("randomBoard", random_board))
    dp.add_handler(CommandHandler("randomThread", random_thread))
    dp.add_handler(CommandHandler("weather", weather, pass_args=True))
    dp.add_handler(CommandHandler("wikired", wiki_red))
    dp.add_handler(CommandHandler("8chanBoard", random_8chan_booard))
    dp.add_handler(CommandHandler("8chanThread", random8_chan_thread, pass_args=True))
    dp.add_handler(CommandHandler("4chanboards", list4_chan_boards))
    dp.add_handler(CommandHandler("8chanboards", list_8_chan_boards))
    dp.add_handler(CommandHandler("get", search_image, pass_args=True, pass_user_data=updater.last_update_id))
    dp.add_handler(CommandHandler("dotaprogames", get_pro_dota_games))
    dp.add_handler(CommandHandler("getTimeZone", get_time_zone, pass_args=True))
    dp.add_handler(CommandHandler("joke", joke))
    dp.add_handler(CommandHandler("simpsonquote", simpsons_quote))
    dp.add_handler(CommandHandler("roll", roll_the_dice, pass_args=True))
    dp.add_handler(CommandHandler("kebab", wikibab))
    dp.add_handler(CommandHandler("call", call))
    dp.add_handler(CommandHandler('kalash', kalash_traidor))
    dp.add_handler(CallbackQueryHandler(chan_4_button))
    dp.add_handler(CommandHandler('wikired_speech', wikired_speech, ))
    dp.add_handler(CommandHandler("ukrania_today", ukrania_today))
    dp.add_handler(CommandHandler("get_dotaprocircuit", get_dota_procircuit))
    dp.add_handler(CommandHandler("ukranian", ukranian))
    dp.add_handler(CommandHandler("donate", donate))
    dp.add_handler(CommandHandler("tts", text_speech, pass_args=True))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
