import enum
import pygame as pg
import sys
from map import *
from player import *
import math
from ghost import *
import random as rad

WIN = (700,650)
FPS = 60

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN)
        pg.display.set_caption('Pacman')
        self.highscore = 0
        self.max_level = 5
        self.level = 0
        self.score = 0
        self.image_menu = pg.image.load('menu.png').convert_alpha()
        self.play_button = pg.image.load('play_button.png')
        self.menu = True
        self.clock = pg.time.Clock()
        # self.new_game()
    def draw_menu(self):
        self.image_menu = pg.transform.scale(self.image_menu,WIN)
        self.screen.blit(self.image_menu,(0,0))
        self.play_button = pg.transform.scale(self.play_button,(200,50))
        self.play_button_rect = self.play_button.get_rect(center = (110,290))
        self.screen.blit(self.play_button,self.play_button_rect)
        pg.display.update()
    def new_game(self):
        self.level_time = pg.time.get_ticks()
        self.color = [(118,238,198),(255,64,64),(0,201,87),(99,99,99),(156,102,31),(69,139,116),(250,235,215)]
        self.highscore_font = pg.font.SysFont('arial',20)
        self.score_font = pg.font.SysFont('arial',20)
        self.restart_font = pg.font.SysFont('arial',50)
        self.gameover_font = pg.font.SysFont('arial',50)
        self.level_font = pg.font.SysFont('arial',50)
        self.time = pg.time.get_ticks()
        self.map = Map(self,self.level)
        # self.player = Player(self,1.5,1.5)
        self.set_player()
        self.foods = []
        self.ghosts = []
        self.create_food()
        self.create_ghosts()
    def set_player(self):
        for i,row in enumerate(self.map.mini_map):
            for j,value in enumerate(row):
                if value == 4:
                    self.player = Player(self,j+0.5,i+0.5,self.score)
                    return
    def draw_level(self):
        level_surface = self.level_font.render(f'LEVEL {str(self.level+1)}',False,(255,255,255))
        level_rect = level_surface.get_rect(center = (280,200))
        self.screen.blit(level_surface,level_rect)
    def draw_game_over(self,string):
        gameover_surface = self.gameover_font.render(string,False,(255,255,255))
        gameover_rect = gameover_surface.get_rect(center = (280,200))
        self.screen.blit(gameover_surface,gameover_rect)
        restart_surface = self.restart_font.render('RESTART',False,(255,255,255))
        self.restart_rect = restart_surface.get_rect(center = (280,300))
        self.screen.blit(restart_surface,self.restart_rect)
    def draw_score(self):
        score_surface = self.score_font.render(f'Score: {str(self.player.point)}',False,(255,255,255))
        score_rect = score_surface.get_rect(center = (560,60))
        self.screen.blit(score_surface,score_rect)
        highscore_surface = self.highscore_font.render(f'High Score: {str(self.highscore)}',False,(255,255,255))
        highscore_rect = score_surface.get_rect(center = (560,30))
        self.screen.blit(highscore_surface,highscore_rect)
    def create_ghosts(self):
        for i,row in enumerate(self.map.mini_map):
            for j,value in enumerate(row):
                if value == 3:
                    color = rad.choice(self.color)
                    self.ghosts.append(Ghost(self,j+0.5,i+0.5,color))
    def create_food(self):
        for i,row in enumerate(self.map.mini_map):
            for j,value in enumerate(row):
                if value != 1 and value != 4:
                    if value == 2:
                        self.foods.append((j,i,'power'))
                    else: self.foods.append((j,i,'normal'))
    def draw_food(self):
        for food in self.foods:
            if food[2] == 'power':
                pg.draw.circle(self.screen,'red',((food[0]+0.5)*self.map.scale,(food[1]+0.5)*self.map.scale),5)
            else:
                pg.draw.circle(self.screen,'white',((food[0]+0.5)*self.map.scale,(food[1]+0.5)*self.map.scale),2)
    def eat_food(self):
        i = 0
        for food in self.foods:
            dist = math.hypot(self.player.pos[0]-food[0]-0.5,self.player.pos[1]-food[1]-0.5)
            if dist <= 0.5:
                if food[2] == 'power':
                    self.time = pg.time.get_ticks()
                    self.player.eat_ghost = True
                self.foods.pop(i)
                i-=1
                self.player.point+=10
            i+=1
        self.player.eating_ghost()
    def update(self):
        self.player.update()
        for ghost in self.ghosts:
            ghost.update()
        self.eat_food()
        if pg.time.get_ticks() - self.time > 5000:
            self.player.eat_ghost = False
        self.highscore = max(self.highscore,self.player.point)
    def draw(self):
        self.screen.fill((0,0,0))
        self.map.draw()
        self.draw_food()
        for ghost in self.ghosts:
            ghost.draw()
        self.player.draw()
        self.draw_score()
        if not self.player.life or len(self.ghosts) == 0 or len(self.foods) == 0:
            if not self.player.life:
                self.draw_game_over('GAME OVER')
            elif self.level == self.max_level-1:
                self.draw_game_over('VICTORY')
            else:
                self.level = (self.level+1)%self.max_level
                self.score = self.player.point
                self.new_game()
        if pg.time.get_ticks()-self.level_time < 2000:
            self.draw_level()
        pg.display.update()
    def run(self):
        while True:
            if self.menu:
                self.draw_menu()
                for e in pg.event.get():
                    if e.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if e.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()
                        if pos[0] > self.play_button_rect.left and pos[0] < self.play_button_rect.right and pos[1] > self.play_button_rect.top and pos[1] < self.play_button_rect.bottom:
                            self.menu = False
                            self.new_game()
            else:
                for e in pg.event.get():
                    if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    if e.type == pg.MOUSEBUTTONDOWN and not self.player.life:
                        pos = pg.mouse.get_pos()
                        if pos[0] > self.restart_rect.left and pos[0] < self.restart_rect.right and pos[1] > self.restart_rect.top and pos[1] < self.restart_rect.bottom:
                            self.new_game()
                    if e.type == pg.MOUSEBUTTONDOWN and (self.level == self.max_level-1) and (len(self.ghosts) == 0 or len(self.foods) == 0):
                        pos = pg.mouse.get_pos()
                        if pos[0] > self.restart_rect.left and pos[0] < self.restart_rect.right and pos[1] > self.restart_rect.top and pos[1] < self.restart_rect.bottom:
                            self.level = 0
                            self.score = 0
                            self.new_game()
                if self.player.life and not((self.level == self.max_level-1) and (len(self.ghosts) == 0 or len(self.foods) == 0)):
                    self.update()
                self.draw()
            self.clock.tick(FPS)
game = Game()
game.run()
