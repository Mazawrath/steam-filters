import requests
import Database
from sys import argv
import json

key = argv[1]


def get_steam_id(vanity_url):
    url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    # defining a params dict for the parameters to be sent to the API
    params = {'key': key, "vanityurl": vanity_url}
    # sending get request and saving the response as response object
    r = requests.get(url=url, params=params)
    data = r.json()
    return data['response']['steamid']


def get_games_owned(steam_id):
    retVar = []
    # api-endpoint
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    # defining a params dict for the parameters to be sent to the API
    params = {'key': key, "steamid": steam_id, 'include_appinfo': False,
              'include_played_free_games': True, }
    r = requests.get(url=url, params=params)
    data = r.json()
    for game_data in data['response']['games']:
        retVar.append(game_data['appid'])
    return retVar


def get_related_games(steam_ids, matching_requirement):
    matching_games = []
    matching_games_count = []
    player_games = []
    for idx, steam_ids in enumerate(steam_ids):
        player_games.append(get_games_owned(steam_ids))
    for i in range(len(player_games)):
        for game in player_games[i]:
            # if game not in player_games[i]:
            #     player_games[0].remove(game)
            # else:
            #     matching_games.append(game)

            # if game in player_games[i]:
            if game not in matching_games:
                matching_games.append(game)
                matching_games_count.append(1)
            else:
                location = matching_games.index(game)
                matching_games_count[location] += 1

    idx = 0
    # for idx, count in enumerate(matching_games_count):
    while (idx < len(matching_games_count)):
        if matching_games_count[idx] < matching_requirement:
            matching_games.pop(idx)
            matching_games_count.pop(idx)
            if idx != 0:
                idx -= 1
        else:
            idx += 1
    return matching_games


def get_games_info(steam_ids, game_ids):
    game_infos = []
    # for game in game_ids:
    url = 'https://store.steampowered.com/api/appdetails?'
    # defining a params dict for the parameters to be sent to the API
    game_list = ""
    for game in game_ids:
        game_list += str(game) + ','
    game_list = game_list[:-1]
    print(game_list)
    params = {'appids': game_list, 'filters': 'basic,price_overview'}
    # sending get request and saving the response as response object
    r = requests.get(url=url, params=params)
    data = r.json()
    print(json.dumps(data))
    # if data['type'] != 'game':
    #     continue
    # name = data['name']

    # game_infos.append([, ])


def update_all_games():
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002"
    params = {'key': key}
    # sending get request and saving the response as response object
    r = requests.get(url=url, params=params)
    data = r.json()
    print(json.dumps(data))

