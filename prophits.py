import requests
import urllib
from datetime import datetime
import csv

BASE_URL = 'https://api.prop-odds.com'
API_KEY = 'VVsRrOkerrHMZKTwbRIYQJmPp9RY6ebZDsVpFZjzaM'


def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    print('Request failed with status:', response.status_code)
    return {}


def get_nba_games():
    date = datetime(2024,2,23)
    query_params = {
        'date': date.strftime('%Y-%m-%d'),
        'tz': 'America/New_York',
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/games/nba?' + params
    return get_request(url)


def get_game_info(game_id):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/game/' + game_id + '?' + params
    return get_request(url)


def get_markets(game_id):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/markets/' + game_id + '?' + params
    return get_request(url)


def get_player_props(game_id, market):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/v1/fantasy_lines/' + game_id + '/' + market + '?' + params
    return get_request(url)


def main():
    games = get_nba_games()
    if len(games['games']) == 0:
        print('No games scheduled for today.')
        return

    # Dictionary to store player stats for each bookie
    player_stats = {}

    # Iterate through games
    for game in games['games']:
        game_id = game['game_id']
        game_info = get_game_info(game_id)
        markets = get_markets(game_id)
        player_props = get_player_props(game_id, 'player_points_over_under')

        # Iterate through players and their stats
        for book in player_props['fantasy_books']:
            bookie_name = book['bookie_key']
            for line in book['market']['lines']:
                player_name = line['participant_name']
                points = line['line']
                stat = book['market']['market_key']

                # Create a key for the player if not exists
                if player_name not in player_stats:
                    player_stats[player_name] = {}

                # Add player's stat for the current bookie
                player_stats[player_name][bookie_name] = points

    # Write player stats to CSV
    with open('player_stats.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Player', 'NameofStat', 'amountOfStatDraftkings',  'amountOfstatPrizepicks', 'amountOfStatUnderdog'])

        for player_name, stats in player_stats.items():
            # Write player's name
            row = [player_name,stat]

            # Check if each bookie has stats for the player
            for bookie in ['draftkings', 'prizepicks','underdog']:
                if bookie in stats:
                    row.extend([stats[bookie]])
                else:
                    row.extend([''])

            # Write the row to CSV
            writer.writerow(row)

if __name__ == '__main__':
    main()



