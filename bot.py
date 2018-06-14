import urllib
from urllib import request
from telegram.ext import Updater, CommandHandler, run_async
import logging
import requests
import wikipedia
import basc_py4chan
import markovify
import re
import json
from random import randint
from telegramBot.lib import py8chan
import telegramBot.src.config as config
import dota2api

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


def get_coords(args):
    location = ' '.join(args)

    GOOGLE_MAPS_API_URL = config.GOOGLE_MAPS_API_URL

    params = {
        'address': location,
        'key': config.GOOGLE_MAPS_API_KEY
    }
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    print(req)
    res = req.json()
    print(res)
    result = res['results'][0]
    print(result)

    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']
    geodata['address'] = result['formatted_address']
    print(geodata)

    return geodata


@run_async
def joke(bot, update):
    try:
        req = requests.get(r'https://icanhazdadjoke.com/slack')
        print(req)
        res = req.json()
        text = (res['attachments'][0]['text'])
        bot.send_message(chat_id=update.message.chat_id,
                         text=text)
    except Exception as e:
        print(e)


@run_async
def get_time_zone(bot, update, args):
    try:
        geodata = get_coords(args)
        lat = geodata['lat']
        lng = geodata['lng']
        address = geodata['address']
        timezone_params = {
            'key': config.timezonekey,
            'format': 'json',
            'by': 'position',
            'lat': lat,
            'lng': lng
        }
        TIMEZONEDB_URL = r'http://api.timezonedb.com/v2/get-time-zone'
        req = requests.get(TIMEZONEDB_URL, timezone_params)
        print(req)
        response = req.json()
        print(response)
        hour = (response['formatted'])
        zone_name = response['zoneName']
        time_zone = response['abbreviation']
        print(hour, zone_name, time_zone)
        bot.send_message(chat_id=update.message.chat_id,
                         text='> Location: ' + address +
                              '\n> Hour: ' + hour +
                              '\n > Zone Name: ' + zone_name +
                              '\n > Time Zone: ' + time_zone)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Location not found')


@run_async
def send_location(bot, update, args):
    try:
        location = ' '.join(args)
        geodata = get_coords(location)
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
        query = ' '.join(args)
        article = wikipedia.page(query)
        bot.send_message(chat_id=update.message.chat_id, text=article.url)
    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Search not found')
        logger.warning('Update "%s" caused error "%s"' % (update, error))


def check4_chan_board(bot, update, args):
    try:
        query = ' '.join(args)
        board = basc_py4chan.Board(query)
        thread_ids = board.get_all_thread_ids()
        bot.send_message(chat_id=update.message.chat_id,
                         text='There are ' + str(len(thread_ids)) + ' active threads on ' + str(query))
    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text='board not found')


@run_async
def random_thread(bot, update, args):
    try:

        query = ' '.join(args)
        board = basc_py4chan.Board(str(query))
        threadIds = board.get_all_thread_ids()
        threadIds = [str(id) for id in threadIds]  # need to do this so str.join below works
        randomThread = randint(0, (len(threadIds) - 1))
        thread = board.get_thread(int(threadIds[randomThread]))
        for f in thread.file_objects():
            bot.send_message(chat_id=update.message.chat_id, text=(f.file_url))
            # print(' Fileurl', f.file_url)
            break
        update.message.reply_text('http://boards.4chan.org/' + str(query) + '/thread/' + str(threadIds[randomThread]))

    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=('board not found'))


@run_async
def random_board(bot, update):
    try:
        randomBoard = boards[randint(0, 68)]
        board = basc_py4chan.board(randomBoard)
        threadIds = board.get_all_thread_ids()
        threadIds = [str(id) for id in threadIds]  # need to do this so str.join below works
        randomThread = randint(0, (len(threadIds) - 1))
        thread = board.get_thread(int(threadIds[randomThread]))

        for f in thread.file_objects():
            bot.send_message(chat_id=update.message.chat_id, text=(f.file_url))
            # print(' Fileurl', f.file_url)
            break
        bot.send_message(chat_id=update.message.chat_id, text=(
                'http://boards.4chan.org/' + str(randomBoard) + '/thread/' + str(threadIds[randomThread])))

    except Exception as exception:
        print(exception)
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id,
                         text=('Error'))


@run_async
def weather(bot, update, args):
    try:
        city = ' '.join(args)
        cities = []
        cities.append(city)
        base_url = config.OPbase_url
        api_key = config.OPapi_key
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
                    update.message.reply_text('City: ' + str(location['name'] +
                                                             '\nTemperature: ' + str(location['main']['temp']) + 'ºC' +
                                                             '\nHumidity: ' + str(location['main']['humidity']) + '%' +
                                                             '\nPressure: ' + str(
                        location['main']['pressure']) + 'hPA' +
                                                             '\nClouds: ' + str(location['clouds']['all']) + ' %'))
        except Exception as exception:

            bot.send_message(chat_id=update.message.chat_id,
                             text=str(exception))
    except requests.exceptions.RequestException as error:
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(error))


def insertTweetQuery(tweet):
    try:
        with config.engine.connect() as con:
            tweet.replace('\'', '\'\'')
            tweet.replace('%', '%%')
            tweet.replace('\"', '\"\"')
            con.execute('INSERT INTO TwitterBot.Wikired_Query (Wikired_Query.TWEET) values (\"' + tweet + '\")')
            print('tweet insertado: ' + tweet)
    except Exception as e:
        print(e)


def wiki_red(bot, update):
    try:
        print('patata')
        con = config.engine.connect()
        tweets = con.execute('SELECT Text FROM Wikired_Data')
        tweetList = []
        for tweet in tweets:
            tweetList.append(str(tweet['Text']))
        text_model = markovify.NewlineText(tweetList, state_size=3)
        modelJson = text_model.to_json()
        reconstituted_model = markovify.NewlineText.from_json(modelJson)
        tweet = reconstituted_model.make_short_sentence(280)
        # print(tweet)
        insertTweetQuery(tweet)
        bot.send_message(chat_id=update.message.chat_id,
                         text=tweet)
    except Exception as exception:
        logger.warning('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(exception))


@run_async
def random8ChanBoard(bot, update):
    try:
        randomBoard = chan8Boards[randint(0, len(chan8Boards))]
        board = py8chan.board(randomBoard)
        threadIds = board.get_all_thread_ids()
        threadIds = [str(id) for id in threadIds]  # need to do this so str.join below works
        randomThread = randint(0, (len(threadIds) - 1))
        thread = board.get_thread(int(threadIds[randomThread]))

        # print('url: ' + 'http://boards.4chan.org/' + str(randomBoard) + '/thread/' + str(threadIds[randomThread]))
        for f in thread.file_objects():
            bot.send_message(chat_id=update.message.chat_id, text=(f.file_url))
            print(' Fileurl', f.file_url)
            break

        bot.send_message(chat_id=update.message.chat_id,
                         text=(
                                 'https://8ch.net/' + str(randomBoard) + '/res/' + str(
                             threadIds[randomThread]) + '.html'))

    except Exception as exception:
        print(exception)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(exception))
        logger.warning('Update "%s" caused error "%s"' % (update, error))


@run_async
def random8_chan_thread(bot, update, args):
    try:
        query = ' '.join(args)
        board = py8chan.Board(str(query))
        threadIds = board.get_all_thread_ids()
        threadIds = [str(id) for id in threadIds]  # need to do this so str.join below works
        randomThread = randint(0, (len(threadIds) - 1))
        thread = board.get_thread(int(threadIds[randomThread]))

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
                         text=str(exception))
        logger.warning('Update "%s" caused error "%s"' % (update, error))


def list8ChanBoards(bot, update):
    try:
        bot.send_message(chat_id=update.message.chat_id,
                         text=chan8Boards)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))
        logger.warning('Update "%s" caused error "%s"' % (update, error))


def list4ChanBoards(bot, update):
    try:
        bot.send_message(chat_id=update.message.chat_id,
                         text=boards)
    except Exception as e:
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))
        logger.warning('Update "%s" caused error "%s"' % (update, error))


def getRawHTML(url):
    try:

        headers = {}
        headers[
            'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        print(e)


def getLinks(html):
    urls = []
    url = re.findall('http[s]?:(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))*', html)
    for link in url:
        if (str(link).__contains__('encrypted') or str(link).__contains__('google') or str(link).__contains__(
                'blogger.com') or str(link).__contains__('gstatic.com') or str(link).__contains__('youtube') or str(
            link).__contains__('schema.org') or str(link).__contains__('http://www.w3.org/2000/svg')):
            print('no')
        else:
            print(link)
            urls.append(link)
    print(len(urls))
    return urls


def get_random_picture(images):
    try:
        random_pic = randint(0, (len(images) - 1))
        if (images[random_pic] == None):
            get_random_picture(images)
        else:
            return images[random_pic]
    except Exception as e:
        print(e)
        findErrorPic()


def findErrorPic():
    files = [r'https://i.imgur.com/NhjZ3B9.jpg', r'https://i.imgur.com/n1ne6Xf.jpg', r'https://i.imgur.com/G7Vwf0z.jpg',
             r'https://i.imgur.com/mmn8sbw.png', r'https://i.imgur.com/kVYqDWM.gif', r'https://i.imgur.com/QbfsniO.jpg',
             r'https://i.imgur.com/QHqCH2w.jpg',
             r'https://i.imgur.com/x0e9mRu.jpg', r'https://i.imgur.com/b1izBqW.png',
             r'https://i.redd.it/266673dajx0z.jpg',
             r'https://cdn.dribbble.com/users/366584/screenshots/2527274/404_1.gif',
             r'https://cdn.dribbble.com/users/469578/screenshots/2597126/404-drib23.gif']
    random = randint(0, len(files) - 1)
    randomImage = files[random]
    return randomImage


@run_async
def searchImage(bot, update, args):
    try:
        print('champiñon')
        if (args != None):
            commandQuery = ' '.join(str(args))
            query = commandQuery.replace(' ', '%20').encode('utf-8')
            url = 'https://www.google.com/search?q=' + str(
                query) + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
            html = getRawHTML(url)
            urls = getLinks(html)
            if (len(urls) < 5):
                update.message.reply_photo(findErrorPic())
            else:
                picture = get_random_picture(urls)
                update.message.reply_text(picture)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='no')

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))
        logger.warning('Update "%s" caused error "%s"' % (update, error))


@run_async
def getProDotaGames(bot, update):
    try:
        api = dota2api.Initialise(config.dotaApi)
        games = api.get_live_league_games()
        leagues = api.get_league_listing()
        heroes = api.get_heroes()
        a = []
        for game in games['games']:
            league_id = game['league_id']
            for league in leagues['leagues']:
                league_name = (league['name'])
                if league['leagueid'] == (league_id) and league['name'] != 'FACEIT League' and league['name']:
                    radiant_team = ''
                    dire_team = ''
                    if 'radiant_team' not in game:
                        radiant_team = 'Radiant'
                    else:
                        radiant_team = game['radiant_team']['team_name']
                    if 'dire_team' not in game:
                        dire_team = 'Dire'
                    else:
                        dire_team = game['dire_team']['team_name']
                    radiant_series_win = game['radiant_series_wins']
                    dire_series_win = game['dire_series_wins']
                    radiant_score = 0
                    dire_score = 0

                    if 'scoreboard' not in game or 'score' not in game['scoreboard']['radiant']:
                        radiant_score = 0
                    else:
                        radiant_score = game['scoreboard']['radiant']['score']

                    if 'scoreboard' not in game or 'score' not in game['scoreboard']['dire']:
                        dire_score = 0
                    else:
                        radiant_score = game['scoreboard']['radiant']['score']
                    game_time = 0
                    if 'scoreboard' not in game or 'duration' not in game['scoreboard']:
                        game_time = 0
                    else:
                        game_time = game['scoreboard']['duration']
                    radiant_net = 0
                    dire_net = 0
                    series = ''
                    if game['series_type'] == 0:
                        series = 'Non-series'
                    elif game['series_type'] == 1:
                        series = 'Best of 3'
                    elif game['series_type'] == 2:
                        series = 'Best of 5'
                    radiant_heroes = []
                    dire_heroes = []
                    if 'scoreboard' not in game or 'picks' not in game['scoreboard']['radiant']:
                        radiant_heroes.append('No heroes yet')
                    else:
                        for hero in game['scoreboard']['radiant']['picks']:
                            hero_id = hero['hero_id']
                            for hero in heroes['heroes']:
                                if hero['id'] == hero_id:
                                    hero_name = hero['localized_name']
                                    radiant_heroes.append(hero_name)
                    if 'scoreboard' not in game or 'picks' not in game['scoreboard']['dire']:
                        dire_heroes.append('No heroes yet')
                    else:
                        for hero in game['scoreboard']['dire']['picks']:
                            hero_id = hero['hero_id']
                            for hero in heroes['heroes']:
                                if hero_id == hero['id']:
                                    dire_heroes.append(hero['localized_name'])
                    radiant_net = 0
                    if 'scoreboard' not in game or 'players' not in game['scoreboard']['radiant']:
                        radiant_net = 0
                    else:
                        for player in game['scoreboard']['radiant']['players']:
                            radiant_net += float(player['net_worth'])
                    dire_net = 0
                    if 'scoreboard' not in game or 'players' not in game['scoreboard']['dire']:
                        dire_net = 0
                    else:
                        for player in game['scoreboard']['dire']['players']:
                            dire_net += float(player['net_worth'])
                    game_info = {
                        'radiant_team_name': radiant_team,
                        'dire_team_name': dire_team,
                        'league_name': league_name,
                        'radiant_series_win': str(radiant_series_win),
                        'dire_series_win': str(dire_series_win),
                        'radiant_score': str(radiant_score),
                        'dire_score': str(dire_score),
                        'radiant_heroes': str(radiant_heroes),
                        'dire_heroes': str(dire_heroes),
                        'total_net': str(radiant_net - dire_net),
                        'time': str(game_time / 60),
                        'series_type': series
                    }
                    message = game_info['league_name'] + '\n' + game_info['radiant_team_name'] + ' vs ' + game_info[
                        'dire_team_name'] + '\n' + 'Score: ' + \
                              game_info['radiant_score'] + '-' + game_info['dire_score'] + '\n' + 'Series type: ' + \
                              game_info[
                                  'series_type'] + '\n' + 'Series Score: ' + game_info[
                                  'radiant_series_win'] + '-' + game_info['dire_series_win'] + '\n' + 'Time: ' + \
                              game_info[
                                  'time'] + '\nGold Difference: ' + game_info['total_net'] + '\n' + game_info[
                                  'radiant_team_name'] + ' Heroes: ' + \
                              game_info['radiant_heroes'] + '\n' + game_info['dire_team_name'] + ' Heroes: ' + \
                              game_info['dire_heroes']
                    print(json.dumps(game_info, indent=2))
                    a.append(message)
                    bot.send_message(chat_id=update.message.chat_id, text=message)

        if len(a) == 0:
            bot.send_message(chat_id=update.message.chat_id,
                             text='No games yet')
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text=str(e))
        logger.warning('Update "%s" caused error "%s"' % (update, error))


@run_async
def simpsons_quote(bot, update):
    try:
        re = requests.get(r'https://frinkiac.com/api/random')
        json_response = re.json()
        print(re)
        print(json_response)
        quotes = ''
        for quote in json_response['Subtitles']:
            quotes += (quote['Content']) + '\n'

        # base url: https://frinkiac.com/img/S09E25/812894/medium.jpg'
        season = json_response['Frame']['Episode']
        timestamp = json_response['Frame']['Timestamp']
        picture = r'https://frinkiac.com/img/' + str(season) + '/' + str(timestamp) + '/medium.jpg'
        print(picture)
        # bot.send_message(chat_id=update.message.chat_id, text=quotes, photo=picture)
        bot.send_photo(chat_id=update.message.chat_id, photo=picture, caption=quotes)

    except Exception as e:
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
    dp.add_handler(CommandHandler("wikired", wiki_red, ))
    dp.add_handler(CommandHandler("8chanBoard", random8ChanBoard))
    dp.add_handler(CommandHandler("8chanThread", random8_chan_thread, pass_args=True))
    dp.add_handler(CommandHandler("4chanboards", list4ChanBoards))
    dp.add_handler(CommandHandler("8chanboards", list8ChanBoards, ))
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
