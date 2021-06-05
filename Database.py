import sqlite3
from sqlite3 import Error

connection = None


def create_connection(path):
    global connection
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")

        # Create the basic table if it doesn't already exist.
        query = """
        CREATE TABLE IF NOT EXISTS game_info (
          app_id INTEGER PRIMARY KEY,
          name VARCHAR(512) NOT NULL,
          store_link VARCHAR(512),
          launch_link VARCHAR(512),
          box_art VARCHAR(512),
          categories VARCHAR(512),
          genres VARCHAR(512)
        );
        """
        __execute_query__(query)
    except Error as e:
        print(f"The error '{e}' occurred")


def __execute_query__(query):
    global connection
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def __execute_read_query__(query):
    global connection
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def update_game(app_id, name, store_link, launch_link, box_art, categories, genres):
    global connection

    # If the game isn't in the database, add it
    if not get_game(app_id):
        query = """
        INSERT INTO game_info("app_id", "name", "store_link", "launch_link", "box_art", "categories", "genres")
        VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")
        """ % (app_id, name, store_link, launch_link, box_art, categories, genres)
    # Update the game if it's already in the database
    else:
        query = """
              UPDATE game_info
              SET "name" = "%s", "box_art" = "%s", "categories" = "%s", "genres" = "%s"
              WHERE app_id = %s;
              """ % (name, box_art, categories, genres, app_id)
    __execute_query__(query)


def get_game(app_id):
    ret_val = __execute_read_query__("SELECT * FROM game_info WHERE app_id = %s;" % app_id)
    if ret_val:
        ret_val = ret_val[0]
        ret_val = {
            "app_id": ret_val[0],
            "name": ret_val[1],
            "store_link": ret_val[2],
            "launch_link": ret_val[3],
            "box_art": ret_val[4],
            "categories": ret_val[5].split(","),
            "genres": ret_val[6].split(",")
        }
        return ret_val
    else:
        return None
