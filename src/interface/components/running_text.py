from __future__ import annotations
import pygame as pg

from src.core.services import input_manager, sound_manager, resource_manager
from src.utils import Logger, GameSettings
from typing import Callable, override
from .component import UIComponent
from src.interface.components import Text

class RunningText(Text):
    text_font: pg.font.Font
    text_surface: pg.Surface
    text_display: str
    color: tuple[int]
    pos_x: int
    pos_y: int
    speed: int
    text_size: int
    text_lenth: int
    x_right: int
    x_left: int
    
    @override
    def __init__(
        self,
        text_display: str, text_size: int, font_path: str, color: tuple[int],
        x: int = 0, y: int = 0, speed: int = 3
    ):
        """speed dafault = 3 """
        not_used = x

        self.x_right = GameSettings.SCREEN_WIDTH
        super().__init__(text_display, text_size, font_path, color, self.x_right, y)
        
        #self.text_display = text_display

        #self.text_size = text_size
        #self.text_lenth = len(self.text_display) * self.text_size * 0.75
        self.text_lenth = self.get_width()
        
        self.x_right = GameSettings.SCREEN_WIDTH
        self.x_left = -(self.text_lenth)
        
        #self.speed = (0 - speed) * GameSettings.TILE_SIZE
        self.speed = -speed
        
    # Text Run
    def text_run(self):
        #if self.pos_x == self.x_right:
            #Logger.info("RunningText appear")
        if self.pos_x <= self.x_left:
            #Logger.info("RunningText completely disappear")
            self.pos_x = self.x_right
            #Logger.info("RunningText appear")
        else:
            self.move_by(self.speed, 0)

    def pos_init(self):
        self.pos_x = self.x_right
    
    @override
    def update(self, dt: float) -> None:
        # Text Run
        #self.text_lenth = len(self.text_display) * self.text_size
        self.x_right = GameSettings.SCREEN_WIDTH
        self.text_lenth = self.get_width() # RunningText problem fixed
        self.x_left = -(self.text_lenth)
        self.text_run()
        
        super().update(dt)
        
    @override
    def draw(self, screen: pg.Surface) -> None:
        super().draw(screen)
    