import json
import random

from telegram.ext import Updater, CommandHandler, run_async, CallbackQueryHandler
import telegram.chataction
import logging
import src.config as config
import src.four_chan
import src.wikired
import src.eight_chan
import src.google_scrapping
import src.online_apis
import src.Dota
import src.RPG
import src.kalash
import src.Artifact

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Pues estoy funcionando')


def help(bot, update):
    update.message.reply_text(
        'My commands are: /wikipedia , /locate , /board , /randomThread, /randomBoard ,/weather, /wikired, /quote')


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


@run_async
def joke(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        text = handler.joke()
        bot.send_message(chat_id=update.message.chat_id,
                         text=text)
    except Exception as e:
        print(e)


@run_async
def get_time_zone(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        data = handler.get_time_zone(args)
        message = ('Location: ' + data['location'] +
                   '\nHour: ' + data['hour'] +
                   '\nZone Name: ' + data['zone_name'] +
                   '\nTime Zone: ' + data['time_zone'])
        bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Location not found')


@run_async
def send_location(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        geodata = handler.get_coords(args)
        print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))

        bot.send_message(chat_id=update.message.chat_id,
                         text='{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
        bot.sendLocation(chat_id=update.message.chat_id, latitude=geodata['lat'], longitude=geodata['lng'])

    except Exception as exception:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Location not found')
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)


def send_wikipedia(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        article = handler.send_wikipedia(args)
        bot.send_message(chat_id=update.message.chat_id, text=article.url)
    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Search not found')
        logger.warning('Update "%s" caused error "%s"' % (update, error))


def check4_chan_board(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.four_chan.FourChanHandler()
        message = handler.check4_chan_board(args)
        bot.send_message(chat_id=update.message.chat_id,
                         text=message)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='board not found')


@run_async
def random_board(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.four_chan.FourChanHandler()
        message, url = handler.random_board()
        print(message, url)
        if '.webm' not in url:
            bot.send_photo(chat_id=update.message.chat_id, photo=url)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            bot.send_message(chat_id=update.message.chat_id, text=url)
            bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=('board not found'))


@run_async
def weather(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        data = handler.weather(args)
        update.message.reply_text(data)
    except Exception as error:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(error))


def wiki_red(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.wikired.Wikired()
        tweet = handler.wiki_red()
        bot.send_message(chat_id=update.message.chat_id,
                         text=tweet)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def wikibab(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.wikired.Wikired()
        tweet = handler.wiki_bab()
        bot.send_message(chat_id=update.message.chat_id,
                         text=tweet)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


@run_async
def random_8chan_booard(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.eight_chan.EightChanHandler()
        message, url = handler.random_8_chan_board()
        print(message, url)
        if '.webm' not in url:
            bot.send_photo(chat_id=update.message.chat_id, photo=url)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            bot.send_message(chat_id=update.message.chat_id, text=url)
            bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=('board not found'))


@run_async
def random8_chan_thread(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.eight_chan.EightChanHandler()
        message, url = handler.random8_chan_thread(args)
        print(message, url)
        if '.webm' not in url:
            bot.send_photo(chat_id=update.message.chat_id, photo=url)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            bot.send_message(chat_id=update.message.chat_id, text=url)
            bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=('board not found'))


def list_8_chan_boards(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.eight_chan.EightChanHandler()
        boards = handler.list_8_chan_boards()
        bot.send_message(chat_id=update.message.chat_id, text=boards)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=('board not found'))


def list4_chan_boards(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.four_chan.FourChanHandler()
        boards = handler.list_4_chan_boards()
        bot.send_message(chat_id=update.message.chat_id,
                         text=boards)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))


@run_async
def search_image(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.google_scrapping.GoogleScrapper(args)
        picture = handler.search_image()
        update.message.reply_text(picture)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))


@run_async
def get_pro_dota_games(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        games = src.Dota.get_pro_dota_games()
        for game in games:
            bot.send_message(chat_id=update.message.chat_id, text=game)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))


@run_async
def simpsons_quote(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        picture, quotes = handler.simpsons_quote()
        bot.send_photo(chat_id=update.message.chat_id, photo=picture, caption=quotes)

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))


def roll_the_dice(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        number = src.RPG.roll_the_dice(args)
        update.message.reply_text(number)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))


@run_async
def random_thread(bot, update):
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
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def add_kalash_betrayal(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.kalash.Kalash()
        status = handler.insert_betrayal(args)
        if status == 1:
            update.message.reply_text("Thanks for reporting it")
        else:
            update.message.reply_text("tu tontolculo no sabes ni reportar @DarkTrainer eso es ban")

    except Exception as e:
        update.message.reply_text("An error ocurred, try again later")
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def show_betrayals(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.kalash.Kalash()
        betrayals = handler.show_betrayal()
        print(len(betrayals))
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(betrayals))

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def chan_4_button(bot, update):
    try:

        query = update.callback_query
        print(query)
        print(query.data)
        handler = src.four_chan.FourChanHandler()
        message, url = handler.random_thread(query.data)
        bot.edit_message_text(text="Selected option: {}".format(query.data) + '\n' + url + '\n' + message,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return query.data

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def kalash_traidor(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        frases_kalash = ['Luego vuelvo.\n(Verano de algun año)', 'U L T R A I C I O N A D O',
                         'Hola chicos, echais un dota?', 'Quiero jugar nyx', 'kalash(traidor)', '*risa de urraca*',
                         'Me tenÃ©is manÃ­a', 'Red, echamos un rainbow?', 'Luego vuelvo. \n(No volverá¡)',
                         'El PUBG es una mierda\n\n*Kalash juega al PUBG*',
                         'Mis amigos me han traicionado por el Fortnite',
                         'Ahora vuelvo \n*Vuelve a la 1 de la mañana cuando ya nos vamos todos*',
                         'Red, bajate el PayDay 2 que jugamos. \n*9 meses después, Red desinstala el PayDay 2 sin haber videojugado*',
                         'Kalash T\'as picat \nKalash: Comeme los huevos',
                         'La paella es comida, a diferencia del durum', 'El durum es una mierda',
                         'Escuchate el album de Unpluged de Nirvana', 'Dejad de meteros con Kurt Cobain, pobrecito',
                         'Dejad de meteros conmigo', 'La nación valenciana',
                         'Echamos un payday 2? Venga chicos, que me lo instalo', 'puto gilipollas el bristleback',
                         '*risa descontrolada ante cualquier gilipollez*',
                         'Me instalo arch linux cada vez que enciendo el pc', 'install gentoo']
        bot.send_message(chat_id=update.message.chat_id,
                         text=frases_kalash[random.randint(0, len(frases_kalash) - 1)])
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def get_pollution(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.online_apis.OnlineApis()
        pollution_params = handler.get_pollution(args)
        message = ''
        for param in pollution_params:
            message += (param + '\n')

        update.message.reply_text(message)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def wikired_speech(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.wikired.Wikired()
        tweet = handler.text_to_speech()
        bot.send_message(chat_id=update.message.chat_id,
                         text=tweet)
        bot.send_audio(chat_id=update.message.chat_id, audio=open('/home/Xiao/telegrambot/ukranian_audio.mp3', 'rb'))

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def ukrania_today(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        handler = src.wikired.Wikired()
        tweet = handler.ukrania_today()
        bot.send_message(chat_id=update.message.chat_id,
                         text=tweet)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def get_dota_procircuit(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        tournaments = src.Dota.get_dota_procircuit()

        bot.send_message(chat_id=update.message.chat_id,
                         text=tournaments)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def get_random_artifact_card(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        random_card = src.Artifact.Artifact()
        card = random_card.get_cards()
        bot.send_message(chat_id=update.message.chat_id,
                         text=card)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def text_speech(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.RECORD_AUDIO)
        handler = src.wikired.Wikired()
        file = handler.tts(args)
        bot.send_voice(chat_id=update.message.chat_id, voice=open('ukranian_audio.mp3', 'rb'))

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str('Try again later'))


def main():
    updater = Updater(config.updater, workers=4)
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
    dp.add_handler(CommandHandler('kalash', kalash_traidor))
    dp.add_handler(CommandHandler('add_betrayal', add_kalash_betrayal, pass_args=True))
    dp.add_handler(CommandHandler('show_betrayal', show_betrayals))
    dp.add_handler(CallbackQueryHandler(chan_4_button))
    dp.add_handler(CommandHandler('get_pollution', get_pollution, pass_args=True))
    dp.add_handler(CommandHandler('wikired_speech', wikired_speech, ))
    dp.add_handler(CommandHandler("ukrania_today", ukrania_today))
    dp.add_handler(CommandHandler("get_dotaprocircuit", get_dota_procircuit))
    dp.add_handler(CommandHandler("get_random_artifactcard", get_random_artifact_card))
    dp.add_handler(CommandHandler("tts", text_speech, pass_args=True))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
