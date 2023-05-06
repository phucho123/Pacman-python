import pygame as pg
import math
from settings import *

from settings import *

class Player:
    def __init__(self,game,x,y,score):
        self.x = x
        self.y = y
        self.game = game
        self.speed = 0.12
        self.dir = 0
        self.flip = False
        self.angle = 0
        self.animation_time = pg.time.get_ticks()
        self.open_mouth = False
        self.last_dir = 0
        self.radius = 0.35
        self.eat_ghost = False
        self.life = True
        self.point = score
    def update(self):
        self.move()
        tmp_list = [[self.radius,self.radius],[self.radius,-self.radius],[-self.radius,self.radius],[-self.radius,-self.radius]]
        for rad in tmp_list:
            x = self.x+self.dir*self.speed*math.cos(self.angle)+rad[0]
            y = self.y+self.dir*self.speed*math.sin(self.angle)+rad[1]
            if self.collision(x,y):
                self.dir = 0
                return
        self.x+=self.dir*self.speed*math.cos(self.angle)
        self.y+=self.dir*self.speed*math.sin(self.angle)
    def move(self):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.dir = -1
            self.angle = 0
        if key[pg.K_RIGHT]:
            self.dir = 1
            self.angle = 0
        if key[pg.K_UP]:
            self.dir = -1
            self.angle = math.pi/2
        if key[pg.K_DOWN]:
            self.dir = 1
            self.angle = math.pi/2
        if self.dir != 0: self.last_dir = self.dir
    def draw_open_mouth(self):
        for i in range(45):
            tmp_angle1 = self.angle+i/30*math.pi/6
            tmp_angle2 = self.angle-i/30*math.pi/6
            pg.draw.line(self.game.screen,'black',(self.x*SCALE,self.y*SCALE),(self.x*SCALE+self.last_dir*math.cos(tmp_angle1)*self.radius*SCALE,self.y*SCALE+self.last_dir*math.sin(tmp_angle1)*self.radius*SCALE),2)
            pg.draw.line(self.game.screen,'black',(self.x*SCALE,self.y*SCALE),(self.x*SCALE+self.last_dir*math.cos(tmp_angle2)*self.radius*SCALE,self.y*SCALE+self.last_dir*math.sin(tmp_angle2)*self.radius*SCALE),2)
            i+=3
    def draw(self):
        pg.draw.circle(self.game.screen,'yellow',(self.x*SCALE,self.y*SCALE),self.radius*SCALE)
        if pg.time.get_ticks()-self.animation_time > 300:
            self.open_mouth = not self.open_mouth
            self.animation_time = pg.time.get_ticks()
        if self.open_mouth:
            self.draw_open_mouth()
    def collision(self,x,y):
        if (int(x),int(y)) in self.game.map.world_map:
            return True
        return False
    def eating_ghost(self):
        i = 0
        for ghost in self.game.ghosts:
            dist = math.hypot(self.x-ghost.x,self.y-ghost.y)
            if dist < self.radius+ghost.radius:
                if self.eat_ghost:
                    self.game.ghosts.pop(i)
                    i-=1
                    self.point+=50
                else:
                    self.life = False
                    break
            i+=1
    @property
    def pos(self):
        return (self.x,self.y)
    
        
    