import pygame


class States():
    def __init__(self):
        self.is_idle = True
        self.is_moving = False
        self.facing_right = False
        self.facing_left = True

        self.is_jumping = False
        self.is_falling = False

        self.is_dead = False
        self.is_attacking = False
        self.is_hit = False
        self.is_aggro = False

    def set_idle(self, state):
        self.is_idle = state
        if state:
            self.is_jumping, self.is_falling, self.is_dead, self.is_attacking, self.is_hit, self.is_aggro = False

    def facing_right(self):
        self.facing_right, self.facing_left = True, False

    def facing_left(self):
        self.facing_left, self.facing_right = True, False

    def set_jumping(self, state):
        self.is_jumping = state
        if state:
            self.is_falling, self.is_dead, self.is_attacking, self.is_hit, self.is_aggro = False

    def set_falling(self, state):
        self.is_falling = state
        if state:
            self.is_jumping, self.is_dead, self.is_attacking, self.is_hit, self.is_aggro = False

    def set_dead(self, state):
        self.is_dead = state
        if state:
            self.is_idle, self.is_jumping, self.is_falling, self.is_attacking, self.is_hit, self.is_aggro = False

    def set_attacking(self, state):
        self.is_attacking = state
        if state:
            self.is_idle, self.is_jumping, self.is_falling, self.is_dead, self.is_hit = False

    def set_damaged(self, state):
        self.is_hit = state
        if state:
            self.is_idle, self.is_jumping, self.is_falling, self.is_dead, self.is_attacking = False

    def set_aggro(self, state):
        self.is_aggro = state
