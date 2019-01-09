import random

import src.config as config
import requests
import wikipedia
import time

from bs4 import BeautifulSoup


class OnlineApis:

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
        city = ' '.join(args)
        # print(city)
        base_url = config.OPbase_url
        api_key = config.OPapi_key
        query = base_url + '?q=%s&units=metric&APPID=%s' % (city, api_key)
        response = requests.get(query)
        if response.status_code != 200:
            print('error')
            return 'Please try again later'
        else:
            weather_data = response.json()
            # print(weather_data)
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
        # print(re)
        # print(json_response)
        quotes = ' '
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
        # print(req)
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
        address = geodata['address']
        timezone_params = {
            'key': config.timezonekey,
            'format': 'json',
            'by': 'position',
            'lat': lat,
            'lng': lng
        }
        req = requests.get(config.TIMEZONEDB_URL, timezone_params)
        # print(req)
        response = req.json()
        # print(response)
        hour = (response['formatted'])
        zone_name = response['zoneName']
        time_zone = response['abbreviation']
        location = response['countryName']
        data = {
            'location': location,
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
        # print(req)
        res = req.json()
        # print(res)
        result = res['results'][0]
        # print(result)

        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['address'] = result['formatted_address']

        print(geodata)

        return geodata

    def get_pollution(self, location):
        try:
            """Given a query, it gets the coordinates of given location using google maps and returns a list of pollution parameters
                 Parameters
                 ----------
                 args : String
                     Location
                 Returns
                 -------
                 Dictionary
                     List with pollution parameters
    
                 """
            coords = self.get_coords(location)

            polution_params = ['bc', 'co', 'no2', 'o3', 'pm10', 'pm25', 'so2']
            data = []
            location_cords = str(coords['lat']) + ',' + str(coords['lng'])
            location_name = (coords['address'])
            data.append(location_name)
            for param in polution_params:
                params = {
                    'format': 'json',
                    'date_to ': time.time(),
                    'limit': 1,
                    'parameter': param,
                    'coordinates': (location_cords),
                    'order_by': 'date',
                    'radius': 3000
                }
                re = requests.get(url=config.pollution_url, params=params)
                extracted_data = re.json()
                if (len(extracted_data['results']) == 0):
                    pass
                else:
                    message = str(extracted_data['results'][0]['parameter']) + ' ' + str(extracted_data['results'][0][
                                                                                             'value']) + ' ' + str(
                        extracted_data['results'][0]['unit'])
                    data.append(message)
            if len(data) > 1:
                return data
            else:
                data[0] = "There are not any public weather station nearby"
                return data
        except Exception as e:
            print(e)

    def make_request(self, url):
        """
        :type url: str
        """
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = requests.get(url=url, headers=headers)
        print(request)
        html = request.content
        return html

    def get_div_matches(self, html, div_class_name):
        soup = BeautifulSoup(html, 'html.parser')
        matches = soup.findAll("div", class_=div_class_name)
        return matches

    def get_card_links(self, matches):
        match_list = []
        for match in matches:
            a = match.find('a')
            url = a.attrs['href']
            match_list.append(url)
            print(url)
        return match_list

    def get_card_info(self, cards):
        for card in cards:
            html = self.make_request(card)
            matches = self.get_div_matches(html, div_class_name='col-md-3 col-sm-12 col-xs-12')
            for match in matches:
                a = match.text

    def get_artifact_random_card(self):
        class_to_find = 'col-md-2 col-sm-3 col-xs-6 '
        card_links = []
        limit = 2
        i = 1
        while i < limit:
            url = 'https://www.playartifact.info/cards/all/?page=' + str(i)
            print('[INFO] Connecting to: ', url)
            html = self.make_request(url)
            matches = self.get_div_matches(html, class_to_find)
            card_list = self.get_card_links(matches)
            print(len(card_list))
            if len(card_list) != 0:
                limit = limit + 1
                i = i + 1
                for card in card_list:
                    card_links.append(card)
            else:
                i = limit

        print(card_links)
        random_number = random.randint(0, len(card_links))
        print(card_links[random_number])
        return card_links[random_number]

