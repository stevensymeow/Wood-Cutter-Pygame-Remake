from __future__ import annotations
import pygame as pg

from src.utils import GameSettings
from src.core.services import input_manager, sound_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
from .whshape import WHShape
from src.interface.components import Text, Overlay, Rectangle, Text
from src.core import GameManager, Game
from src.data.info import GameInfo

class FallingObject(WHShape):
    # Pos and size
    x_left: int
    x_right: int
    pos: int
    
    # Color
    color: tuple[int, int, int]
    hitbox_color: tuple[int, int, int]
    
    # Fall
    y_dropped: int
    
    # Is falling
    falling: bool
    
    # Game manager
    game_manager: GameManager
    
    # Move
    moved: bool
    started_moving: bool
    
    def __init__(self, game_manager: GameManager, 
                 width: int, height: int,
                 color: tuple[int, int, int], hitbox_color: tuple[int, int, int],
                 can_drag: bool = False, pos: int = -1):
        """
        Yes, this is the tree branch
        """
        # Game manager
        self.game_manager = game_manager
        
        # Pos and size
        pcx, pcy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT / 2
        
        self.width = width
        self.height = height
        
        self.x_left = pcx - GameInfo.bark_width/2 - GameInfo.branch_width/2
        self.x_right = pcx + GameInfo.bark_width/2 + GameInfo.branch_width/2
        self.pos = pos
        
        # pos init
        if self.pos == -1:
            self.x = self.x_left
        elif self.pos == 1:
            self.x = self.x_right
        else: # should not happen
            self.x = pcx
        self.pos_init()
        
        # Color
        self.color = color
        self.hitbox_color = hitbox_color
        
        # Show
        self.falling = True
        
        # Fall
        self.y_dropped = 0
        
        # Move
        self.moved = False
        self.started_moving = False
        
        super().__init__(color=color, 
                         x=self.x, y=0, 
                         width=self.width, height=self.height, 
                         can_drag=can_drag)
    
    def pos_init(self):
        self.y = 0
        self.set_pos(self.x, self.y)
        self.y_dropped = 0
    
    @override
    def update(self, dt: float, move: bool = False) -> None:
        match (self.game_manager.state):
            case Game.Entered:
                pass
            case Game.Playing:
                hy = GameSettings.SCREEN_HEIGHT
                if self.y == 0:
                    sound_manager.play_sound("pop.wav")
                if self.y < hy:
                    # Fall
                    drop = GameInfo.gravity
                    self.move_by(0, drop)
                    self.y_dropped += drop
                    # Hit the player
                    if self.hitbox.colliderect(self.game_manager.wood_cutter.hitbox):
                        self.when_hit_player()
                else:
                    if self.falling:
                        if self.y >= hy:
                            self.when_hit_ground()
                # Move to left or right
                if move and (not self.moved) and self.y_dropped >= GameSettings.SCREEN_HEIGHT/2:
                    if not self.started_moving:
                        self.started_moving = True
                        sound_manager.play_sound(self.game_manager.curr_lv.move_sound)
                    if self.pos == -1:
                        if self.x < self.x_right:
                            self.move_by(GameInfo.branch_move_speed, 0)
                        else:
                            self.x = self.x_right
                            self.pos = 1
                            self.moved = True
                    elif self.pos == 1:
                        if self.x > self.x_left:
                            self.move_by(-GameInfo.branch_move_speed, 0)
                        else:
                            self.x = self.x_left
                            self.pos = -1
                            self.moved = True

        super().update(dt)
    
    def when_hit_ground(self):
        """When tounch the ground"""
        pass
    
    def when_hit_player(self):
        """When hit(touch) the player(wood cutter)"""
        pass
     
    @override
    def draw(self, screen: pg.Surface, show: bool = True) -> None:
        if self.falling and show:
            super().draw(screen)
        
        if GameSettings.DRAW_HITBOXES:
            pg.draw.rect(screen, self.hitbox_color, self.hitbox, 2)
