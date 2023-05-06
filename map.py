import pygame as pg
from settings import *
from level import *
_ = 0
levels = [level1,level2,level3,level4,level5,level6]
class Map:
    def __init__(self,game,level):
        self.game = game
        self.mini_map = levels[level]
        self.world_map = {}
        self.scale = SCALE
        self.get_map()
    def get_map(self):
        for j,row in enumerate(self.mini_map):
            for i,value in enumerate(row):
                if value == 1:
                    self.world_map[(i,j)] = value
    def draw(self):
        for pos in self.world_map:
            if (pos[0]-1,pos[1]) not in self.world_map:
                pg.draw.line(self.game.screen,'blue',(pos[0]*self.scale,pos[1]*self.scale),(pos[0]*self.scale,(pos[1]+1)*self.scale),4)
            if (pos[0]+1,pos[1]) not in self.world_map:
                pg.draw.line(self.game.screen,'blue',((pos[0]+1)*self.scale,pos[1]*self.scale),((pos[0]+1)*self.scale,(pos[1]+1)*self.scale),4)
            if (pos[0],pos[1]-1) not in self.world_map:
                pg.draw.line(self.game.screen,'blue',((pos[0])*self.scale,pos[1]*self.scale),((pos[0]+1)*self.scale,pos[1]*self.scale),4)
            if (pos[0],pos[1]+1) not in self.world_map:
                pg.draw.line(self.game.screen,'blue',(pos[0]*self.scale,(pos[1]+1)*self.scale),((pos[0]+1)*self.scale,(pos[1]+1)*self.scale),4)


