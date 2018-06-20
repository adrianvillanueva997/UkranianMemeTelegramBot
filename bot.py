from telegram.ext import Updater, CommandHandler, run_async
import logging
import requests
import telegramBot.src.config as config
import telegramBot.src.four_chan
import telegramBot.src.wikired
import telegramBot.src.eight_chan
import telegramBot.src.google_scrapping
import telegramBot.src.online_apis
import telegramBot.src.Dota

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
        handler = telegramBot.src.online_apis.OnlineApis()
        text = handler.joke()
        bot.send_message(chat_id=update.message.chat_id,
                         text=text)
    except Exception as e:
        print(e)


@run_async
def get_time_zone(bot, update, args):
    try:
        handler = telegramBot.src.online_apis.OnlineApis()
        data = handler.get_time_zone(args)
        message = ('Location: ' + data['address'] +
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
        handler = telegramBot.src.online_apis.OnlineApis()
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
        handler = telegramBot.src.online_apis.OnlineApis()
        article = handler.send_wikipedia(args)
        bot.send_message(chat_id=update.message.chat_id, text=article.url)
    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Search not found')
        logger.warning('Update "%s" caused error "%s"' % (update, error))


def check4_chan_board(bot, update, args):
    try:
        handler = telegramBot.src.four_chan.FourChanHandler()
        message = handler.check4_chan_board(args)
        bot.send_message(chat_id=update.message.chat_id,
                         text=message)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='board not found')


@run_async
def random_thread(bot, update, args):
    try:
        handler = telegramBot.src.four_chan.FourChanHandler()
        message, url = handler.random_thread(args)
        print(message, url)
        if '.webm' not in url:
            bot.send_photo(chat_id=update.message.chat_id, photo=url)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            bot.send_message(chat_id=update.message.chat_id, text=url + '\n' + message)
            bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=('board not found'))


@run_async
def random_board(bot, update):
    try:
        handler = telegramBot.src.four_chan.FourChanHandler()
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
        handler = telegramBot.src.online_apis.OnlineApis()
        data = handler.weather(args)
        update.message.reply_text(data)
    except Exception as error:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(error))


def wiki_red(bot, update):
    try:
        handler = telegramBot.src.wikired.Wikired()
        tweet = handler.wiki_red()
        bot.send_message(chat_id=update.message.chat_id,
                         text=tweet)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(exception))


@run_async
def random_8chan_booard(bot, update):
    try:
        handler = telegramBot.src.eight_chan.EightChanHandler()
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
        handler = telegramBot.src.eight_chan.EightChanHandler()
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
        handler = telegramBot.src.eight_chan.EightChanHandler()
        boards = handler.list_8_chan_boards()
        bot.send_message(chat_id=update.message.chat_id, text=boards)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=('board not found'))


def list4ChanBoards(bot, update):
    try:
        handler = telegramBot.src.four_chan.FourChanHandler()
        boards = handler.list_4_chan_boards()
        bot.send_message(chat_id=update.message.chat_id,
                         text=boards)
    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))


@run_async
def searchImage(bot, update, args):
    try:
        handler = telegramBot.src.google_scrapping.GoogleScrapper(args)
        picture = handler.search_image()
        update.message.reply_text(picture)

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))


@run_async
def getProDotaGames(bot, update):
    try:
        games = telegramBot.src.Dota.get_pro_dota_games()
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
        handler = telegramBot.src.online_apis.OnlineApis()
        picture, quotes = handler.simpsons_quote()
        bot.send_photo(chat_id=update.message.chat_id, photo=picture, caption=quotes)

    except Exception as e:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))


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
    dp.add_handler(CommandHandler("randomThread", random_thread, pass_args=True))
    dp.add_handler(CommandHandler("weather", weather, pass_args=True))
    dp.add_handler(CommandHandler("wikired", wiki_red))
    dp.add_handler(CommandHandler("8chanBoard", random_8chan_booard))
    dp.add_handler(CommandHandler("8chanThread", random8_chan_thread, pass_args=True))
    dp.add_handler(CommandHandler("4chanboards", list4ChanBoards))
    dp.add_handler(CommandHandler("8chanboards", list_8_chan_boards))
    dp.add_handler(CommandHandler("get", searchImage, pass_args=True, pass_user_data=updater.last_update_id))
    dp.add_handler(CommandHandler("dotaprogames", getProDotaGames))
    dp.add_handler(CommandHandler("getTimeZone", get_time_zone, pass_args=True))
    dp.add_handler(CommandHandler("joke", joke))
    dp.add_handler(CommandHandler("simpsonquote", simpsons_quote))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
