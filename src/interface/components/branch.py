from __future__ import annotations
import pygame as pg

from src.utils import GameSettings
from src.core.services import input_manager, sound_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
from .whshape import WHShape, Shape
from src.interface.components import Text, Overlay, Rectangle, Text
from src.core import GameManager, Game
from .falling_object import FallingObject
from src.data.info import GameInfo
import random

class Branch(FallingObject):
    # Pos and size
    x_left: int
    x_right: int
    pos: int
    
    # Color
    color: tuple[int, int, int]
    
    # Fall
    y_dropped: int
    
    # Game manager
    game_manager: GameManager
    
    # Move
    do_move: bool
    
    def __init__(self, game_manager: GameManager, can_drag: bool = False, pos: int = -1, do_move: bool = True):
        """
        Yes, this is the tree branch
        """
        # Game manager
        self.game_manager = game_manager
        
        # Pos and size
        pcx, pcy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT / 2
        
        self.width = GameInfo.branch_width
        self.height = GameInfo.branch_height
        
        # Color
        self.color = (204, 122, 0)
        self.hitbox_color = (255, 0, 0)
        
        super().__init__(game_manager=game_manager,  
                         width=self.width, height=self.height, 
                         color=self.color, hitbox_color=self.hitbox_color,
                         can_drag=can_drag,
                         pos=pos)

        # Move
        #self.do_move = True if (random.randint(1, 100) < 50) else False
        self.do_move = do_move
    
    @override
    def update(self, dt: float) -> None:
        branch_move = self.game_manager.curr_lv.branch_move and self.do_move
        super().update(dt, move=branch_move)
    
    @override
    def when_hit_ground(self):
        sound_manager.play_sound("crash.wav")
        self.falling = False
        self.game_manager.fallen_branches += 1
    
    def when_hit_player(self):
        self.game_manager.end_game()
        sound_manager.play_sound("Punch.wav")
        sound_manager.play_sound("Punch1.wav")
        #sound_manager.play_sound("strongpunch.wav")
    
    @override
    def draw_to_surface(self):
        self.draw_shape(Shape.Rectangle)
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        super().draw(screen)
