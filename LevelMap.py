import pygame

class LevelMap():
    def __init__(self):


    def load_map(map):
        f = open(map + '.txt', 'r')
        map_data = f.read()
        f.close()
        map_data = map_data.split('\n')
        game_map = []
        for chunk in map_data:
            game_map.append(list(chunk))
        return game_map