import requests
from bs4 import BeautifulSoup
import random


class Artifact():
    def __init__(self):
        pass

    def __make_request(self, url):
        """
        :type url: str
        """
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = requests.get(url=url, headers=headers)
        print(request)
        html = request.content
        return html

    def __get_div_matches(self, html, div_class_name):
        soup = BeautifulSoup(html, 'html.parser')
        matches = soup.findAll("div", class_=div_class_name)
        return matches

    def __get_card_links(self, matches):
        match_list = []
        for match in matches:
            a = match.find('a')
            url = a.attrs['href']
            match_list.append(url)
            print(url)
        return match_list

    def get_card_info(self, cards):
        for card in cards:
            html = self.__make_request(card)
            matches = self.__get_div_matches(html, div_class_name='col-md-3 col-sm-12 col-xs-12')
            for match in matches:
                a = match.text

    def get_cards(self):
        class_to_find = 'col-lg-15 col-md-3 col-sm-4 col-xs-6 '
        card_links = []
        limit = 2
        i = 1
        while i < limit:
            url = 'https://www.artiguild.com/cards/all/?page=' + str(i)
            print('[INFO] Connecting to: ', url)
            html = self.__make_request(url)
            matches = self.__get_div_matches(html, class_to_find)
            card_list = self.__get_card_links(matches)
            print(len(card_list))
            if len(card_list) != 0:
                limit = limit + 1
                i = i + 1
                for card in card_list:
                    card_links.append(card)
            else:
                i = limit

        return card_links[random.randint(0, len(card_links) - 1)]
