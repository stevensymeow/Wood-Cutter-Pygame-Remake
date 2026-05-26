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

class Gem(FallingObject):
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
    
    def __init__(self, game_manager: GameManager, can_drag: bool = False, pos: int = -1):
        """
        Yes, this is the tree branch
        """
        # Game manager
        self.game_manager = game_manager
        
        # Pos and size
        pcx, pcy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT / 2
        
        self.width = GameInfo.gem_width
        self.height = GameInfo.gem_height
        
        # Color
        self.color = (255, 0, 0)
        self.hitbox_color = (255, 0, 255)
        
        super().__init__(game_manager=game_manager,  
                         width=self.width, height=self.height, 
                         color=self.color, hitbox_color=self.hitbox_color,
                         can_drag=can_drag,
                         pos=pos)
    
    @override
    def update(self, dt: float) -> None:
        super().update(dt)
    
    @override
    def when_hit_ground(self):
        sound_manager.play_sound("Squish Pop.wav")
        self.falling = False
    
    def when_hit_player(self):
        sound_manager.play_sound("eat.wav")
        self.game_manager.collected_gems += 1
        self.falling = False
    
    @override
    def draw_to_surface(self):
        self.draw_shape(Shape.Oval)
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        super().draw(screen)
