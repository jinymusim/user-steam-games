from jinja2 import Environment, FileSystemLoader
from api_calls import *
from user_data import *
import os

def display_games(user: UserData, games):
    result_filename = "user_game.html"
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'content', 'templates')))
    template = env.get_template('template.html')
    context = {
        'user' : user,
        'games' : games
    }
    with open(result_filename, mode="w", encoding="utf-8") as results:
        results.write(template.render(context))
        

if __name__ == "__main__":
    manager = UserDataManager()
    jinymusims_data = manager.get_user_data(user='jinymusim')
    my_games = APICalls.get_player_games(jinymusims_data)[:10]
    for game in my_games:
        APICalls.get_game_images(game)
    display_games(jinymusims_data, my_games)