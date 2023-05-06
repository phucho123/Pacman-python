import pygame as pg
import math
import random as rad
from settings import *

class Ghost:
    def __init__(self,game,x,y,color = 'red'):
        self.game = game
        self.x,self.y = x,y
        self.dir = 1
        self.angle = 0
        self.speed = 0.12
        self.color = color
        self.radius = 0.4
        self.prev_move = ''
        self.time = pg.time.get_ticks()
    @property
    def pos(self):
        return (self.x,self.y)
    def move(self,key):
        if key == 'right':
            self.dir = 1
            self.angle = 0
        if key == 'left':
            self.dir = -1
            self.angle = 0
        if key == 'up':
            self.dir = -1
            self.angle = math.pi/2
        if key == 'down':
            self.dir = 1
            self.angle = math.pi/2
    def check_collision(self,key):
        self.move(key)
        tmp_list = [[self.radius,self.radius],[self.radius,-self.radius],[-self.radius,self.radius],[-self.radius,-self.radius]]
        for rad in tmp_list:
            x = self.x+self.dir*self.speed*math.cos(self.angle)+rad[0]
            y = self.y+self.dir*self.speed*math.sin(self.angle)+rad[1]
            if self.collision(x,y):
                return True
        return False
    def collision(self,x,y):
        if (int(x),int(y)) in self.game.map.world_map:
            return True
        return False
    def moverment(self):
        keys = ['right','left','up','down']
        ways = []
        for key in keys:
            if not self.check_collision(key):
                ways.append(key)
        if self.prev_move == '': self.prev_move = ways[0]
        elif self.prev_move in ways and pg.time.get_ticks() - self.time < 1000: self.prev_move = self.prev_move
        else:
            if len(ways) == 1: self.prev_move = ways[0]
            else:
                tmp = []
                for way in ways:
                    if (self.prev_move == 'right' and way == 'left' or self.prev_move == 'left' and way == 'right' or self.prev_move == 'up' and way == 'down' or self.prev_move == 'down' and way == 'up'):
                        continue
                    else:
                        tmp.append(way)
                self.prev_move = rad.choice(tmp)
            if pg.time.get_ticks() - self.time > 1000:
                self.time= pg.time.get_ticks()
        self.move(self.prev_move)
        self.x+=self.dir*math.cos(self.angle)*self.speed
        self.y+=self.dir*math.sin(self.angle)*self.speed
    def update(self):
        self.moverment()
    def draw(self):
        color = self.color
        if self.game.player.eat_ghost:
            color = 'blue'
        pg.draw.circle(self.game.screen,color,(self.x*SCALE,self.y*SCALE),self.radius*SCALE)
        

