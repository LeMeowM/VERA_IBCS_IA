import pygame


class AreaManager:
    def __init__(self, rooms):
        self.room_index = 0
        # rooms contains room manager objects
        self.rooms = rooms
        self.cur_room = self.rooms[self.room_index]

    def set_room(self, room_index):
        self.room_index = room_index
        self.cur_room = self.rooms[self.room_index]

    def add_room(self, room):
        self.rooms.append(room)
        room.set_room_index(len(self.rooms)-1)

    def draw(self, display, scroll):
        self.cur_room.draw(display, scroll)

    def draw_map(self, display, scroll):
        self.cur_room.room_map.draw_map(display, scroll)

    def map_collision(self, rect, movement):
        return self.cur_room.room_map.map_collision(rect, movement)

    def update(self, anim_count):
        self.cur_room = self.rooms[self.room_index]
        self.cur_room.update(anim_count)
