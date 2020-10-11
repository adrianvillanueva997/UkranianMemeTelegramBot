import random

from pyowm import OWM

import src.config as config
import requests
import wikipedia
import time

from bs4 import BeautifulSoup


class OnlineApis:

    @staticmethod
    def weather(args):
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
        owm = OWM(config.OPapi_key)
        obs = owm.weather_at_place(args)
        w = obs.get_weather()
        # reg = owm.city_id_registry()
        data = {
            'humidity': w.get_humidity()
            , 'temperature': w.get_temperature('celsius')
            , 'wind': w.get_wind()
            , 'clouds': w.get_clouds()
            , 'pressure': w.get_pressure()
        }
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
                if len(extracted_data['results']) == 0:
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
