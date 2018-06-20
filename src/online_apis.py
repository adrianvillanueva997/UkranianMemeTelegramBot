import telegramBot.src.config as config
import requests
import wikipedia


class OnlineApis():

    def weather(self, args):
        """Connects to openWeather and returns the weather from given location
            Parameters
            ----------
            args : String
                Location

            Returns
            -------
            String
                Data extracted from JSON
            """
        print(args)
        city = ''.join(args)
        cities = []
        cities.append(city)
        base_url = config.OPbase_url
        api_key = config.OPapi_key
        query = base_url + '?q=%s&units=metric&APPID=%s' % (city, api_key)
        response = requests.get(query)
        if response.status_code != 200:
            print('error')
            return 'Please try again later'
        else:
            weather_data = response.json()
            print(weather_data)
            location = weather_data
            data = ('City: ' + str(location['name'] +
                                   '\nTemperature: ' + str(
                location['main']['temp']) + 'ºC' +
                                   '\nHumidity: ' + str(
                location['main']['humidity']) + '%' +
                                   '\nPressure: ' + str(
                location['main']['pressure']) + 'hPA' +
                                   '\nClouds: ' + str(location['clouds']['all']) + ' %'))
            return data

    def simpsons_quote(self):
        """Gets a random quote + caption from the largest Simpsons database
            Parameters
            ----------
            args : None

            Returns
            -------
            String
                picture url and quote from that scene

            """
        re = requests.get(config.simpsons_url)
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
        return picture, quotes

    def joke(self):
        """Gets a random dad joke (usually it is pretty bad, but who cares?)
            Parameters
            ----------
            args : None

            Returns
            -------
            String
                Joke

            """
        req = requests.get(config.joke_url)
        print(req)
        res = req.json()
        text = (res['attachments'][0]['text'])
        return text

    def get_time_zone(self, args):
        """Given a certain location, connects to an online api and returns the local time and timezone about that location
            Parameters
            ----------
            args : String
                Location

            Returns
            -------
            Dictionary
                Useful data from the received Json

            """
        geodata = self.get_coords(args)
        lat = geodata['lat']
        lng = geodata['lng']
        timezone_params = {
            'key': config.timezonekey,
            'format': 'json',
            'by': 'position',
            'lat': lat,
            'lng': lng
        }
        req = requests.get(config.TIMEZONEDB_URL, timezone_params)
        print(req)
        response = req.json()
        print(response)
        hour = (response['formatted'])
        zone_name = response['zoneName']
        time_zone = response['abbreviation']
        data = {
            'hour': hour,
            'zone_name': zone_name,
            'time_zone': time_zone
        }
        return data

    def send_wikipedia(self, args):
        """Returns a wikipedia article given a query
            Parameters
            ----------
            args : String
                Query

            Returns
            -------
            String
                url of that wikipedia page

            """
        query = ' '.join(args)
        article = wikipedia.page(query)
        return article

    def get_coords(self, args):
        """Given a query, google maps returns the coordenates from the query
            Parameters
            ----------
            args : String
                Location
            Returns
            -------
            Dictionary
                Dictionary with useful information from Google Maps Api

            """
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
