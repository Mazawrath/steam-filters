import requests
import Database
from sys import argv
import json

key = argv[1]


def get_steam_id(vanity_url):
    url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    params = {'key': key, "vanityurl": vanity_url}
    r = requests.get(url=url, params=params)
    data = r.json()
    return data['response']['steamid']


def get_games_owned(steam_id):
    ret_var = []
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {'key': key, "steamid": steam_id, 'include_appinfo': False,
              'include_played_free_games': True, }
    r = requests.get(url=url, params=params)
    data = r.json()
    for game_data in data['response']['games']:
        ret_var.append(game_data['appid'])
    return ret_var


def get_related_games(steam_ids, matching_requirement):
    matching_games = []
    matching_games_count = []
    player_games = []
    # Get each player's list of owned games
    for idx, steam_ids in enumerate(steam_ids):
        player_games.append(get_games_owned(steam_ids))
    # Go through each steam user's list of owned games
    for i in range(len(player_games)):
        for game in player_games[i]:
            # If a game is not on the matching games list, add it
            if game not in matching_games:
                matching_games.append(game)
                matching_games_count.append(1)
            # If a game is already on the list, increment the count for total users that own the game by 1
            else:
                location = matching_games.index(game)
                matching_games_count[location] += 1

    idx = 0
    # Traverse the matching games list until the end is reached
    # (This while needs to be done since we don't know how long the list will be by the end since any game that is
    # not owned by enough players is removed
    while idx < len(matching_games_count):
        # If a game isn't owned by enough players, remove it from the list and look at the same index again
        if matching_games_count[idx] < matching_requirement:
            matching_games.pop(idx)
            matching_games_count.pop(idx)
            if idx != 0:
                idx -= 1
        # Game is owned by enough players, go to the next game
        else:
            idx += 1
    return matching_games


def get_game_info(game_id):
    game_infos = []
    url = 'https://store.steampowered.com/api/appdetails?'
    params = {'appids': game_id}
    r = requests.get(url=url, params=params)
    data = r.json()

    if data is not None and data[str(game_id)]['success']:
        return data[str(game_id)]['data']
    else:
        return None


def update_all_games():
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002"
    params = {'key': key}
    r = requests.get(url=url, params=params)
    data = r.json()
    # Traverse through every single Steam app
    for game in data['applist']['apps']:
        # Get detailed info for each app
        game_info = get_game_info(game['appid'])
        # Only add an app if there is actually data in game_info and it is a game
        if game_info is not None and game_info['type'] == 'game':
            categories = []
            try:
                for category in game_info['categories']:
                    categories.append(category['description'])
            except KeyError:
                print("Categories not found!\n" + json.dumps(game_info))
            genres = []
            try:
                for genre in game_info['genres']:
                    genres.append(genre['description'])
            except KeyError:
                print("Genres not found!\n" + json.dumps(game_info))
            store_link = "https://store.steampowered.com/app/" + str(game['appid']) + "/"
            launch_link = "steam://rungameid/" + str(game['appid'])
            box_art = "https://steamcdn-a.akamaihd.net/steam/apps/" + str(game['appid']) + "/library_600x900_2x.jpg"
            name = game_info['name']
            name = name.replace('"', '\'\'')
            # If a game doesn't have box art, replace it with the next best thing.
            if requests.get(box_art).status_code != 200:
                box_art = "https://cdn.akamai.steamstatic.com/steam/apps/" + str(game['appid']) + "/header.jpg"
            Database.update_game(game['appid'], name, store_link, launch_link, box_art, ",".join(categories), ",".join(genres))


def get_matching_games_info(steam_ids, matching_games):
    ret_val = {}
    games_owned = []
    for steam_id in steam_ids:
        games_owned.append(get_games_owned(steam_id))
    for app_id in matching_games:
        game_info = Database.get_game(app_id)
        print(game_info)
