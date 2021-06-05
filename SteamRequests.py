import requests
import Database
from sys import argv
import json
from time import sleep

key = argv[1]


def get_steam_id(vanity_url):
    url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    params = {'key': key, "vanityurl": vanity_url}
    attempts = 0
    while attempts <= 10:
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            break
        else:
            print("(Likely) rate limited!")
            attempts += 1
            sleep(90)
    data = response.json()
    return data['response']['steamid']


def get_games_owned(steam_id):
    ret_var = []
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {'key': key, "steamid": steam_id, 'include_appinfo': False,
              'include_played_free_games': True, }
    attempts = 0
    while attempts <= 10:
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            break
        else:
            print("(Likely) rate limited!")
            attempts += 1
            sleep(90)
    data = response.json()
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
    attempts = 0
    while attempts <= 10:
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            break
        else:
            print("(Likely) rate limited!")
            attempts += 1
            sleep(90)
    data = response.json()

    if data is not None and data[str(game_id)]['success']:
        return data[str(game_id)]['data']
    else:
        return None


def __update_database__(game_info):
    categories = []
    if 'categories' in game_info:
        for category in game_info['categories']:
            categories.append(category['description'])
    else:
        print("Categories not found!\n" + json.dumps(game_info))
    genres = []
    if 'genres' in game_info:
        for genre in game_info['genres']:
            genres.append(genre['description'])
    else:
        print("Genres not found!\n" + json.dumps(game_info))
    name = game_info['name'].replace('"', '\'\'')
    store_link = "https://store.steampowered.com/app/" + str(game_info['steam_appid']) + "/"
    launch_link = "steam://rungameid/" + str(game_info['steam_appid'])
    box_art = "https://steamcdn-a.akamaihd.net/steam/apps/" + str(game_info['steam_appid']) + "/library_600x900_2x.jpg"
    # If a game doesn't have box art, replace it with the next best thing.
    if requests.get(box_art).status_code != 200:
        box_art = "https://cdn.akamai.steamstatic.com/steam/apps/" + str(game_info['steam_appid']) + "/header.jpg"
    Database.update_game(game_info['steam_appid'], name, store_link, launch_link, box_art, ",".join(categories),
                         ",".join(genres))


def update_games(update_existing):
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002"
    params = {'key': key}
    r = requests.get(url=url, params=params)
    data = r.json()
    print(r.status_code)
    # Traverse through every single Steam app
    for game in data['applist']['apps']:
        print(game)
        if update_existing and not get_game_info(game['appid']):
            print("Game already exists!")
            continue
        # Get detailed info for each app
        game_info = get_game_info(game['appid'])
        # Only add an app if there is actually data in game_info and it is a game or mod
        if game_info and (game_info['type'] == 'game' or game_info['type'] == 'mod'):
            __update_database__(game_info)


def get_matching_games_info(steam_ids, matching_games):
    games_owned = []

    ret_val = {"categories": [], "genres": [], "games": []}

    for steam_id in steam_ids:
        games_owned.append(get_games_owned(steam_id))
    for app_id in matching_games:
        game_info = Database.get_game(app_id)
        if not game_info:
            print(str(app_id) + " not found!")
            continue

        # Create a list of every category, if any aren't in there, add them
        for category in game_info['categories']:
            if category not in ret_val['categories']:
                ret_val['categories'].append(category)
        # Create a list of every genre, if any aren't in there, add them
        for genre in game_info['genres']:
            if genre not in ret_val['genres']:
                ret_val['genres'].append(genre)

        # Game not found in database, try to find it
        # if not game_info:
        ret_info = {
            "app_id": game_info['app_id'],
            "name": game_info['name'],
            "store_link": game_info['store_link'],
            "launch_link": game_info['launch_link'],
            "box_art": game_info['box_art'],
            "categories": game_info['categories'],
            "genres": game_info['genres']
        }
        ret_val["games"].append(ret_info)

    return json.dumps(ret_val)
