from __future__ import annotations
import pygame as pg

from src.utils import GameSettings
from src.core.services import input_manager, sound_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
from src.interface.components import Text, Overlay, Rectangle, Oval, Text
from src.core import GameManager, Game
from src.data.info import GameInfo
from src.utils.definition import RGBColor

class WoodCutter(UIComponent):
    # Pos and size
    x_left: int
    x_right: int
    x: int
    y: int
    pos_x: int
    pos_y: int
    width: int
    line_width: int
    
    hline: Rectangle # |
    vline: Rectangle # _
    
    # Color
    color: RGBColor
    
    # Hitbox
    hitbox: pg.Rect
    
    # GG
    GG_text: Text
    
    # Game manager
    game_manager: GameManager
    
    # Invincible
    invincible: bool
    inv_oval: Oval
    
    def __init__(self, game_manager: GameManager):
        # Game manager
        self.game_manager = game_manager
        
        # Pos and size
        pcx, pcy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT / 2
        hy = GameSettings.SCREEN_HEIGHT
        self.width = GameInfo.wood_cutter_width
        self.line_width = 2
        
        self.dx = GameInfo.bark_width/2 + self.width/4
        self.x_left = pcx - self.dx
        self.x_right = pcx + self.dx
        self.x = self.x_left
        
        self.y_bottom = hy - self.width/2
        self.y_top = self.width/2
        self.y = self.y_bottom
        
        self.pos = -1
        
        self.color = self.game_manager.curr_lv.player_color
        
        self.hline = Rectangle(self.color, self.x, self.y, self.line_width, self.width)
        self.vline = Rectangle(self.color, self.x, self.y, self.width, self.line_width)
        
        # Hitbox
        self.hitbox = pg.Rect(0, 0, self.width, self.width)
        self.hitbox.center = (self.x, self.y)
        
        # GG
        self.GG_text = Text("GG", self.width, "CambriaBold.ttf", (255, 0, 0), self.x-self.width/2, self.y-self.width/2)
        
        # Invincible
        self.invincible = False
        self.inv_oval = Oval((255, 255, 0), self.x, self.y, self.width, self.width)
        self.inv_oval.set_alpha(100)
        
    def set_color(self, color: RGBColor):
        self.color = color
        self.hline.set_color(color)
        self.vline.set_color(color)
    
    def do_cut(self):
        pcx = GameSettings.SCREEN_WIDTH/2
        left_condition = input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a) or \
        (input_manager.mouse_down(1) and input_manager.mouse_pos[0] < pcx)
        right_condition = input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d) or \
        (input_manager.mouse_down(1) and input_manager.mouse_pos[0] > pcx)
        
        if self.pos == -1:
            if right_condition:
                self.go_right()
            elif left_condition:
                self.go_left()
        elif self.pos == 1:
            if left_condition:
                self.go_left()
            elif right_condition:
                self.go_right()
        
        curr_lv = self.game_manager.curr_lv
        gravity = curr_lv.gravity
        if gravity > 0:
            self.y = self.y_bottom
        else:
            self.y = self.y_top
            
        if self.game_manager.state == Game.Playing:
            self.hline.set_pos(self.x, self.y)
            self.vline.set_pos(self.x, self.y)
            degree = 8
            self.hline.rotate(degree*self.pos*gravity)
            self.vline.rotate(degree*self.pos*gravity)
            
            # Invicible
            self.inv_oval.set_pos(self.x, self.y)
    
    def go_left(self):
        self.pos = -1
        self.x = self.x_left
    
    def go_right(self):
        self.pos = 1
        self.x = self.x_right
    
    def pos_init(self):
        self.x = self.x_left
        gravity = self.game_manager.curr_lv.gravity
        if gravity > 0:
            self.y = self.y_bottom
        else:
            self.y = self.y_top
        
        self.hline.set_pos(self.x, self.y)
        self.vline.set_pos(self.x, self.y)
        self.hline.set_angle()
        self.vline.set_angle()
        
        # Invicible
        self.inv_oval.set_pos(self.x, self.y)
        
        # Hitbox
        self.hitbox = pg.Rect(0, 0, self.width, self.width)
        self.hitbox.center = (self.x, self.y)
    
    @override
    def update(self, dt: float) -> None:
        self.hline.update(dt)
        self.vline.update(dt)
        
        match (self.game_manager.state):
            case Game.Entered:
                self.pos_init()
                self.invincible = False
            case Game.Playing:
                # Do Cut
                self.do_cut()
                
                # Hitbox
                self.hitbox = pg.Rect(0, 0, self.width, self.width)
                self.hitbox.center = (self.x, self.y)
        
        # Invincible
        self.inv_oval.set_pos(self.x, self.y)
        self.inv_oval.update(dt)
        
        # GG
        self.GG_text.set_pos(self.x-self.GG_text.get_width()/2, self.y-self.width/2)
        self.GG_text.update(dt)
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        if self.game_manager.state != Game.GG:
            self.hline.draw(screen)
            self.vline.draw(screen)
            
            # Invincible
            if self.invincible:
                self.inv_oval.draw(screen)
        else:
            # GG
            self.GG_text.draw(screen)
        
        if GameSettings.DRAW_HITBOXES:
            pg.draw.rect(screen, (0, 0, 255), self.hitbox, 2)
            
    