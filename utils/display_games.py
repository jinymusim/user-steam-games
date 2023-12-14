from jinja2 import Environment, FileSystemLoader
from api_calls import *
from user_data import *
import os
import re

def display_games(user: UserData, games):
    result_dict = 'website'
    result_filename = os.path.join('website', "index.html")
    if not os.path.exists(result_dict):
        os.mkdir(result_dict)
        
    if not os.path.exists(os.path.join(result_dict, 'games')):
        os.mkdir(os.path.join(result_dict, 'games'))
    
    for game in games:
        game['href_site'] = os.path.join('games', re.sub( r'[<>:"/\\\|\?\*\s]+','_', f"{game['name']}.html" ))
        game['site_pos'] = os.path.join(result_dict,'games', re.sub( r'[<>:"/\\\|\?\*\s]+','_', f"{game['name']}.html" ))
    game_hours = sum([game['playtime_forever'] for game in games])
    
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'content', 'templates')))
    template = env.get_template('template.html')
    context = {
        'user' : user,
        'games' : games,
        'sum_hours' : game_hours
    }
    with open(result_filename, mode="w", encoding="utf-8") as results:
        results.write(template.render(context))
        
    template = env.get_template('template_game.html')
    for game in games:
        context = {
        'game' : game
        }
        with open(game['site_pos'], mode="w", encoding="utf-8") as results:
            results.write(template.render(context))
        

if __name__ == "__main__":
    manager = UserDataManager()
    jinymusims_data = manager.get_user_data(user='jinymusim')
    my_games = APICalls.get_player_games(jinymusims_data)
    for game in my_games:
        APICalls.get_game_images(game)
    display_games(jinymusims_data, my_games)