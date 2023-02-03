import pygame
from Level.LevelManagerClass import LevelManager


class AreaManager:
    def __init__(self, rooms: list):
        self.room_index: int = 0
        # rooms contains room manager objects
        self.rooms: list = rooms
        self.cur_room: LevelManager = self.rooms[self.room_index]
        self.set_room_indexes()

    def set_room(self, room_index: int) -> None:
        self.room_index = room_index
        self.cur_room = self.rooms[self.room_index]

    def set_room_indexes(self) -> None:
        i = 0
        for room in self.rooms:
            room.set_room_index(i)
            i += 1

    def add_room(self, room: LevelManager) -> None:
        self.rooms.append(room)
        room.set_room_index(len(self.rooms)-1)

    def draw(self, display: pygame.Surface, scroll: list):
        self.cur_room.draw(display, scroll)

    def draw_map(self, display: pygame.Surface, scroll: list) -> None:
        self.cur_room.level_map.draw_map(display, scroll)

    def map_collision(self, rect: pygame.Rect, movement: list) -> None:
        return self.cur_room.level_map.map_collision(rect, movement)

    def update(self, anim_count: int)-> None:
        self.cur_room = self.rooms[self.room_index]
        self.cur_room.update(anim_count)
