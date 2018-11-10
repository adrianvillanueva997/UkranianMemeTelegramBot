import json

import dota2api

api = dota2api.Initialise('97A38E228CA666D466455D64C85DEE9C')
games = api.get_live_league_games()
leagues = api.get_league_listing()
heroes = api.get_heroes()


a = []



def b():
    for game in games['games']:
        print(game)
        league_id = game['league_id']
        for league in leagues['leagues']:
            league_name = (league['name'])
            if league['leagueid'] == (league_id) and league['name']:
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
                match_id = game['match_id']
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
                    'series_type': series,
                    'match_id': str(match_id)
                }
                print(json.dumps(game_info, indent=2))
                message = game_info['league_name'] + '\n' + game_info['radiant_team_name'] + 'vs' + game_info[
                    'dire_team_name'] + '\n' + 'Score: ' + \
                          game_info['radiant_score'] + ' ' + game_info['dire_score'] + '\n' + '\nGame ID: ' + game_info[
                              'match_id'] + '\nSeries type: ' + \
                          game_info[
                              'series_type'] + '\n' + 'Series Score: ' + game_info[
                              'radiant_series_win'] + ' -' + '\n' + 'Time: ' + game_info[
                              'time'] + 'Gold Difference: ' + game_info['total_net'] + '\n' + game_info[
                              'radiant_team_name'] + ' Heroes: ' + \
                          game_info['radiant_heroes'] + '\n' + game_info['dire_team_name'] + ' Heroes: ' + \
                          game_info['dire_heroes']

                print(message)
