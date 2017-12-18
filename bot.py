from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import logging
import requests
import wikipedia
import basc_py4chan
import pymysql
import markovify
import re
from random import randint
from lib import py8chan

hostname = ''
user = ''
password = ''
database = ''
port = 1

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

boards = ['3', 'a', 'aco', 'adv', 'an', 'asp', 'b', 'bant', 'biz', 'c', 'cgl', 'ck', 'cm', 'd', 'diy', 'e', 'f',
          'fa',
          'fit', 'g', 'gd', 'gif', 'h', 'hc', 'his', 'hm', 'hr', 'i', 'ic', 'int', 'jp', 'k', 'lgbt', 'lit',
          'm', 'mlp',
          'mu', 'n', 'news', 'o', 'out', 'p', 'po', 'pol',
          'qa', 'gat', 'r', 'r9k', 's', 's4s', 'sci', 'soc', 'sp', 't', 'tg', 'toy', 'trash', 'trv', 'tv', 'u',
          'v',
          'vg', 'vp', 'vr', 'w', 'wsg', 'wsr', 'x', 'y']

chan8Boards = ['pol', 'v', 'leftypol', 'b', 'tv', 'a', 'christian', 'tech', 'co', 'hgg', 'k', 'newsplus', 'r9k',
               'n',
               'brit', 'tg', 'monster', 'asmr', 'cuteboys', 'cow', '4chon', 'fur', '4chon', 'sudo', 'loli',
               'aus',
               'htg', 'animus', 'vore', 'egy', 'erp', 'homosuck', 'shamedsluts', 'abdl', 'abdl', 'pone',
               'hypno',
               'strek', 'newbrit', 'test', 'zoo', 'mu', 'fit', 'mexicali', 'waifuist', 'russian', 'tijuana',
               'u', '2hu',
               'd']


def start(bot, update):
    update.message.reply_text('Pues estoy funcionando')


def help(bot, update):
    update.message.reply_text(
        'My commands are: /wikipedia , /locate , /board , /randomThread, /randomBoard ,/weather, /wikired, /quote')


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def sendLocation(bot, update, args):
    try:
        location = ' '.join(args)
        GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

        params = {
            'address': location
        }
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()

        result = res['results'][0]

        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['address'] = result['formatted_address']

        print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
        bot.send_message(chat_id=update.message.chat_id,
                         text='{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
        bot.sendLocation(chat_id=update.message.chat_id, latitude=geodata['lat'], longitude=geodata['lng'])

    except Exception as exception:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Location not found')
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)


def sendWikipedia(bot, update, args):
    try:
        query = ' '.join(args)
        article = wikipedia.page(query)
        bot.send_message(chat_id=update.message.chat_id, text=article.url)
    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Search not found')


def check4ChanBoard(bot, update, args):
    try:
        query = ' '.join(args)
        board = basc_py4chan.Board(query)
        thread_ids = board.get_all_thread_ids()
        str_thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
        # print('There are', len(thread_ids), 'active threads on ' + query)
        bot.send_message(chat_id=update.message.chat_id,
                         text='There are ' + str(len(thread_ids)) + ' active threads on ' + str(query))
    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='board not found')


def randomThread(bot, update, args):
    try:

        query = ' '.join(args)

        board = basc_py4chan.Board(str(query))

        threadIds = board.get_all_thread_ids()

        threadIds = [str(id) for id in threadIds]  # need to do this so str.join below works

        # print('There are', len(threadIds), 'active threads on /' + randomBoard + '/:', ', '.join(threadIds))

        randomThread = randint(0, (len(threadIds) - 1))

        # print(threadIds[randomThread])

        thread = board.get_thread(int(threadIds[randomThread]))

        # print('url: ' + 'http://boards.4chan.org/' + str(randomBoard) + '/thread/' + str(threadIds[randomThread]))
        for f in thread.file_objects():
            bot.send_message(chat_id=update.message.chat_id, text=(f.file_url))
            # print(' Fileurl', f.file_url)
            break
        bot.send_message(chat_id=update.message.chat_id, text=(
            'http://boards.4chan.org/' + str(query) + '/thread/' + str(threadIds[randomThread])))

    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Board not found')


def randomBoard(bot, update):
    try:
        b = basc_py4chan.get_all_boards()

        randomBoard = boards[randint(0, 68)]

        board = basc_py4chan.board(randomBoard)

        threadIds = board.get_all_thread_ids()

        threads = []

        threadIds = [str(id) for id in threadIds]  # need to do this so str.join below works

        # print('There are', len(threadIds), 'active threads on /' + randomBoard + '/:', ', '.join(threadIds))

        randomThread = randint(0, (len(threadIds) - 1))

        # print(threadIds[randomThread])

        thread = board.get_thread(int(threadIds[randomThread]))

        topic = thread.topic

        # print('url: ' + 'http://boards.4chan.org/' + str(randomBoard) + '/thread/' + str(threadIds[randomThread]))
        for f in thread.file_objects():
            bot.send_message(chat_id=update.message.chat_id, text=(f.file_url))
            # print(' Fileurl', f.file_url)
            break
        bot.send_message(chat_id=update.message.chat_id, text=(
            'http://boards.4chan.org/' + str(randomBoard) + '/thread/' + str(threadIds[randomThread])))

    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=exception)


def weather(bot, update, args):
    try:
        city = ' '.join(args)
        cities = []
        cities.append(city)
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        api_key = '5991f4bcb0884409212e0e4d6ff2c60c'  # << Get your API key (APPID) here: http://openweathermap.org/appid
        query = base_url + '?q=%s&units=metric&APPID=%s' % (city, api_key)
        try:
            response = requests.get(query)
            if response.status_code != 200:
                bot.send_message(chat_id=update.message.chat_id,
                                 text='City not found')
            else:
                weather_data = response.json()
                for city in cities:
                    location = weather_data
                    bot.send_message(chat_id=update.message.chat_id, text=(
                        'City: ' + str(location['name'] +
                                       '\nTemperature: ' + str(location['main']['temp']) + 'ºC' +
                                       '\nHumidity: ' + str(location['main']['humidity']) + '%' +
                                       '\nPressure: ' + str(location['main']['pressure']) + 'hPA' +
                                       '\nClouds: ' + str(location['clouds']['all']) + ' %')))
        except Exception as exception:

            bot.send_message(chat_id=update.message.chat_id,
                             text=exception)
    except requests.exceptions.RequestException as error:
        bot.send_message(chat_id=update.message.chat_id,
                         text=error)


def wikiRed(bot, update):
    try:
        con = pymysql.connect(host=hostname, user=user, password=password, port=port, database=database)
        cursor = con.cursor()
        cursor.execute('SELECT `Text` FROM TwitterBot.WikiRed')
        rows = cursor.fetchall()
        tweets = []
        for row in rows:
            newRow = str(row).replace('(\'', '')
            updatedRow = str(newRow).replace('\',)', '')
            tweets.append(updatedRow)
            # print(updatedRow)

        randomIndex = randint(0, (len(tweets) - 1))
        bot.send_message(chat_id=update.message.chat_id,
                         text=tweets[randomIndex])
        # print(tweets[randomIndex])
        con.close()
    except Exception as exception:
        bot.send_message(chat_id=update.message.chat_id,
                         text=exception)


def getShit():
    try:
        randomBoard = randint(0, (len(boards) - 1))
        board = basc_py4chan.Board(boards[randomBoard])
        threads = board.get_all_thread_ids()
        randomThread = randint(0, len(threads))
        thread = board.get_thread(threads[randomThread])
        topic = thread.topic
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', topic.comment)
        insert4ChanShitPost(cleantext)
    except Exception as exception:
        print(exception)


def insert4ChanShitPost(shit):
    try:
        db = pymysql.connect(host=hostname, user=user, password=password, port=port, database=database)
        cursor = db.cursor()
        query = 'INSERT into 4chanData (Text) VALUES ' + '(\'' + shit + '\')'
        cursor.execute(query)
        db.commit()
        print(shit)
        db.close()
    except Exception as exception:
        print(exception)


def shitPost(bot, update):
    try:
        con = pymysql.connect(host=hostname, user=user, password=password, port=port, database=database)
        cursor = con.cursor()
        cursor.execute('SELECT `Text` FROM TwitterBot.4chanData')
        rows = cursor.fetchall()
        shitPosting = []
        for row in rows:
            newRow = str(row).replace('(\'', '')
            updatedRow = str(newRow).replace('\',)', '')
            shitPosting.append(updatedRow)
        text_model = markovify.NewlineText(shitPosting)
        shitPostSupreme = text_model.make_short_sentence(140)
        test = str(shitPostSupreme).replace('&gt;', '')
        nuevoTest = str(test).replace('&#039;', '\'')
        con.close()
        getShit()
        bot.send_message(chat_id=update.message.chat_id,
                         text=nuevoTest)
    except Exception as e:
        print(e)


def random8ChanBoard(bot, update):
    try:

        randomBoard = chan8Boards[randint(0, len(chan8Boards))]

        board = py8chan.board(randomBoard)

        threadIds = board.get_all_thread_ids()

        threads = []

        threadIds = [str(id) for id in threadIds]  # need to do this so str.join below works

        # print('There are', len(threadIds), 'active threads on /' + randomBoard + '/:', ', '.join(threadIds))

        randomThread = randint(0, (len(threadIds) - 1))

        # print(threadIds[randomThread])

        thread = board.get_thread(int(threadIds[randomThread]))

        topic = thread.topic

        # print('url: ' + 'http://boards.4chan.org/' + str(randomBoard) + '/thread/' + str(threadIds[randomThread]))
        for f in thread.file_objects():
            bot.send_message(chat_id=update.message.chat_id, text=(f.file_url))
            print(' Fileurl', f.file_url)
            break

        bot.send_message(chat_id=update.message.chat_id,
                         text=(
                             'https://8ch.net/' + str(randomBoard) + '/res/' + str(threadIds[randomThread]) + '.html'))

    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Board not found')


def random8ChanThread(bot, update, args):
    try:

        query = ' '.join(args)

        board = py8chan.Board(str(query))

        threadIds = board.get_all_thread_ids()

        threadIds = [str(id) for id in threadIds]  # need to do this so str.join below works

        # print('There are', len(threadIds), 'active threads on /' + randomBoard + '/:', ', '.join(threadIds))

        randomThread = randint(0, (len(threadIds) - 1))

        # print(threadIds[randomThread])

        thread = board.get_thread(int(threadIds[randomThread]))

        # print('url: ' + 'http://boards.4chan.org/' + str(randomBoard) + '/thread/' + str(threadIds[randomThread]))
        for f in thread.file_objects():
            bot.send_message(chat_id=update.message.chat_id, text=(f.file_url))
            print(' Fileurl', f.file_url)
            break

        bot.send_message(chat_id=update.message.chat_id,
                         text=(
                             'https://8ch.net/' + str(query) + '/res/' + str(threadIds[randomThread]) + '.html'))

    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Board not found')


def list8ChanBoards(bot, update):
    try:
        bot.send_message(chat_id=update.message.chat_id,
                         text=chan8Boards)
    except Exception as e:
        print(e)


def list4ChanBoards(bot, update):
    try:
        bot.send_message(chat_id=update.message.chat_id,
                         text=boards)
    except Exception as e:
        print(e)


def main():
    updater = Updater("?????????????????????????????????")

    dp = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("locate", sendLocation, pass_args=True))
    dp.add_handler(CommandHandler("wikipedia", sendWikipedia, pass_args=True))
    dp.add_handler(CommandHandler("board", check4ChanBoard, pass_args=True))
    dp.add_handler(CommandHandler("randomBoard", randomBoard))
    dp.add_handler(CommandHandler("randomThread", randomThread, pass_args=True))
    dp.add_handler(CommandHandler("weather", weather, pass_args=True))
    dp.add_handler(CommandHandler("wikired", wikiRed, ))
    dp.add_handler(CommandHandler("8chanBoard", random8ChanBoard))
    dp.add_handler(CommandHandler("8chanThread", random8ChanThread, pass_args=True))
    dp.add_handler(CommandHandler("4chanboards", list4ChanBoards))
    dp.add_handler(CommandHandler("8chanboards", list8ChanBoards, ))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


main()
