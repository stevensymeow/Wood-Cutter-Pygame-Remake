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
    
    # Show
    show: bool
    
    # Game manager
    game_manager: GameManager
    
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
        self.show = True
        
        # Fall
        self.y_dropped = 0
        
        super().__init__(color=color, 
                         x=self.x, y=0, 
                         width=self.width, height=self.height, 
                         can_drag=can_drag)
    
    def pos_init(self):
        self.y = 0
        self.set_pos(self.x, self.y)
        self.y_dropped = 0
    
    @override
    def update(self, dt: float) -> None:
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
                    if self.show:
                        if self.y >= hy:
                            self.when_hit_ground()
        
        super().update(dt)
    
    def when_hit_ground(self):
        """When tounch the ground"""
        pass
    
    def when_hit_player(self):
        """When hit(touch) the player(wood cutter)"""
        pass
     
    @override
    def draw(self, screen: pg.Surface) -> None:
        if self.show:
            super().draw(screen)
        
        if GameSettings.DRAW_HITBOXES:
            pg.draw.rect(screen, self.hitbox_color, self.hitbox, 2)
