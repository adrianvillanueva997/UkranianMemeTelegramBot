import requests
from bs4 import BeautifulSoup
import re


def get_pro_dota_games():
    """Live pro dota games
        Parameters
        ----------
        args : None

        Returns
        -------
        List
            String list with useful dota pro games 322
        """
    headers = {'User-Agent': 'Mozilla/5.0'}
    re = requests.get(r'https://api.opendota.com/api/live', headers)
    re2 = requests.get(r'https://api.opendota.com/api/leagues', headers)
    re3 = requests.get(r'https://api.opendota.com/api/heroes', headers)
    games = re.json()
    leagues = re2.json()
    heroes = re3.json()
    live_games = []
    for game in games:
        if game['league_id'] != 0:
            league_name = ''
            spectators = game['spectators']
            radiant_name = ''
            dire_name = ''
            if 'team_name_radiant' not in game:
                radiant_name = 'Radiant'
            else:
                radiant_name = game['team_name_radiant']
            if 'team_name_dire' not in game:
                dire_name = 'Dire'
            else:
                dire_name = game['team_name_dire']
            radiant_score = game['radiant_score']
            dire_score = game['dire_score']
            gold_diference = game['radiant_lead']
            radiant_heroes = []
            dire_heroes = []
            for league in leagues:
                if game['league_id'] == league['leagueid']:
                    league_name = (league['name'])
                    if league['tier'] == 'professional':
                        for player in game['players']:
                            for hero in heroes:
                                hero_name = ''
                                if player['hero_id'] == hero['id']:
                                    for hero in heroes:
                                        if 'team_name' not in player:
                                            pass
                                        elif player['hero_id'] == hero['id']:
                                            hero_name = (hero['localized_name'])
                                            if player['team_name'] == radiant_name:
                                                radiant_heroes.append(hero_name)
                                            else:
                                                dire_heroes.append(hero_name)

                    game_dict = {
                        'league_name': league_name,
                        'spectators': str(spectators),
                        'radiant_name': radiant_name,
                        'dire_name': dire_name,
                        'radiant_heroes': str(radiant_heroes),
                        'dire_heroes': str(dire_heroes),
                        'radiant_score': str(radiant_score),
                        'dire_score': str(dire_score),
                        'gold_difference': str(gold_diference),

                    }
                    message = game_dict['league_name'] + '\n' + game_dict['radiant_name'] + ' vs ' + game_dict[
                        'dire_name'] \
                              + '\n' + game_dict['radiant_score'] + ' - ' + game_dict[
                                  'dire_score'] + '\n' + 'Gold Difference: ' + game_dict['gold_difference'] + '\n' + \
                              game_dict['radiant_name'] + ' Heroes: ' + game_dict['radiant_heroes'] + '\n' + \
                              game_dict['dire_name'] + ' Heroes: ' + game_dict['dire_heroes'] + '\nSpectators: ' + \
                              game_dict['spectators']
                    live_games.append(message)
    return live_games


def get_dota_procircuit():
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = requests.get(r'https://www.dota2.com/procircuit', headers)
    html = request.content
    soup = BeautifulSoup(html, 'html.parser')
    major_blocks = soup.findAll("div", {'class': 'scheduleElement major'})
    minor_blocks = soup.findAll("div", {'class': 'scheduleElement minor'})
    regex = r'<img class="flag" src=".*"\/>'
    minors = []
    majors = []
    for minor in minor_blocks:
        soup = BeautifulSoup(str(minor), 'html.parser')
        date = soup.find('span', {'class': 'columnContent dateColumn'})
        date = str(date).replace('<span class="columnContent dateColumn">', '')
        date = date.replace('</span>', '')

        location = soup.find('span', {'class': 'columnContent locationColumn'})
        location = str(location).replace('<span class="columnContent locationColumn">', '')
        location = location.replace('</span>', '')
        location = re.sub(regex, '', location)
        prize = soup.find('span', {'class': 'columnContent prizeColumn'})
        prize = str(prize).replace('<span class="columnContent prizeColumn">', '')
        prize = prize.replace('</span>', '')
        points = soup.find('span', {'class': 'columnContent pointsColumn'})
        points = str(points).replace('<span class="columnContent pointsColumn">', '')
        points = points.replace('</span>', '')
        organizer = soup.find('span', {'class': 'columnContent organizerColumn'})
        organizer = str(organizer).replace(
            '<span class="columnContent organizerColumn"><img class="tournamentLogo" src="https://steamcdn-a.akamaihd.net/apps/dota2/images/majorsminors/organizers/',
            '')
        organizer = organizer.replace('.png"/></span>', '')
        organizer = organizer.replace('<span class="columnContent organizerColumn"><div class="PendingLogo">', '')
        organizer = organizer.replace('</div></span>', '')
        data = {
            'date': date,
            'location': location,
            'prize': prize,
            'points': points,
            'organizer': organizer
        }
        minors.append(data)

    for major in major_blocks:
        soup = BeautifulSoup(str(major), 'html.parser')
        date = soup.find('span', {'class': 'columnContent dateColumn'})
        date = str(date).replace('<span class="columnContent dateColumn">', '')
        date = date.replace('</span>', '')

        location = soup.find('span', {'class': 'columnContent locationColumn'})
        location = str(location).replace('<span class="columnContent locationColumn">', '')
        location = location.replace('</span>', '')
        location = re.sub(regex, '', location)
        prize = soup.find('span', {'class': 'columnContent prizeColumn'})
        prize = str(prize).replace('<span class="columnContent prizeColumn">', '')
        prize = prize.replace('</span>', '')
        points = soup.find('span', {'class': 'columnContent pointsColumn'})
        points = str(points).replace('<span class="columnContent pointsColumn">', '')
        points = points.replace('</span>', '')
        organizer = soup.find('span', {'class': 'columnContent organizerColumn'})
        organizer = str(organizer).replace(
            '<span class="columnContent organizerColumn"><img class="tournamentLogo" src="https://steamcdn-a.akamaihd.net/apps/dota2/images/majorsminors/organizers/',
            '')
        organizer = organizer.replace('.png"/></span>', '')
        organizer = organizer.replace('<span class="columnContent organizerColumn"><div class="PendingLogo">', '')
        organizer = organizer.replace('</div></span>', '')
        data = {
            'date': date,
            'location': location,
            'prize': prize,
            'points': points,
            'organizer': organizer
        }
        majors.append(data)

    tournaments = {
        'minors': minors,
        'majors': majors
    }
    print(tournaments)
    message = '==MAJORS=='
    for major in tournaments['majors']:
        message += '\n' + major['date'] + '\n' + major['location'] + '\n' + major['prize'] + '\n' + major[
            'points'] + '\n' + \
                   major['organizer'] + '\n--------------'
    message += '\n==MINORS=='
    for minor in tournaments['minors']:
        message += '\n' + minor['date'] + '\n' + minor['location'] + '\n' + minor['prize'] + '\n' + minor[
            'points'] + '\n' + \
                   minor['organizer'] + '\n--------------'

    return message


if __name__ == '__main__':
    get_dota_procircuit()
