from user_data import *
from PIL import Image
import requests
import io
import os
import numpy as np
import re

class APICalls:
    
    @staticmethod
    def get_player_games(user_data: UserData):
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={user_data.API_KEY}&steamid={user_data.USER_ID}&include_appinfo=True&format=json"
        request_result = requests.get(url)
        if not request_result.ok:
            return []
        else:
            games =  request_result.json()['response']['games']
            for game in games:
                game['playtime_forever']//=60
            games = sorted(games, key=lambda x: x['playtime_forever'], reverse=True)
            return games
        
    def get_game_images(game_data: dict):
        name = re.sub(r'[<>:"/\\\|\?\*]+','',game_data['name']) 
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'content','images', f"{name}.jpeg")):
            print(f"{game_data['name']}: Cached image!")
            game_data['img_icon'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'content','images', f"{name}.jpeg")) 
           
        else:
            url=f"https://media.steampowered.com/steamcommunity/public/images/apps/{game_data['appid']}/{game_data['img_icon_url']}.jpg"
            request_result = requests.get(url)
            if not request_result.ok:
                print("Couldn't get image")
                game_data['img_icon'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'content','images', "placeholder.jpeg"))
            else:
                image = Image.open(io.BytesIO(request_result.content))
                image.save(os.path.join(os.path.dirname(__file__), 'content','images', f"{name}.jpeg"))
                game_data['img_icon'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'content','images', f"{name}.jpeg"))
        game_data['img_icon_rel_path'] = os.path.relpath(game_data['img_icon'], os.path.join(os.path.dirname(__file__), '..', 'website'))
                
        
        
        
if __name__ == "__main__":
    manager = UserDataManager()
    jinymusims_data = manager.get_user_data(user='jinymusim')
    my_games = APICalls.get_player_games(jinymusims_data)
    for game in my_games:
        APICalls.get_game_images(game)
    print(my_games)