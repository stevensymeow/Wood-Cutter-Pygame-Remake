from __future__ import annotations
import pygame as pg

from src.utils import GameSettings
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent

class Overlay(UIComponent):
    overlay_surface: pg.Surface
    color_alpha: tuple[int, int, int, int]
    pos: tuple[int, int]
    pos_x: int
    pos_y: int
    width: int
    height: int
    size: tuple[int, int]
    prev_size: tuple[int, int]
    is_frame: bool
    
    def __init__(
        self,
        color_alpha: tuple[int, int, int, int],
        pos: tuple[int, int] = (0, 0),
        width: int = None, height: int = None
    ):
        self.pos = pos
        self.pos_x, self.pos_y = pos[0], pos[1]
        self.color_alpha = color_alpha
        
        self.width = width
        self.height = height
        self.is_frame = self.width != None and self.height != None
        
        self.size = (0, 0)
        self.prev_size = (0, 0)
    
    def set_width(self, width: int):
        self.width = width
        
    def set_height(self, height: int):
        self.height = height
        
    def set_color(self, color: tuple[int, int, int]):
        self.color_alpha = color + (self.color_alpha[3], )
    
    def move_by(self, dx: int, dy: int) -> None:
        self.pos_x += dx
        self.pos_y += dy
        self.pos = (self.pos_x, self.pos_y)

    def set_pos(self, x: int, y: int) -> None:
        self.pos_x, self.pos_y = x, y
        self.pos = (self.pos_x, self.pos_y)
    
    @override
    def update(self, dt: float) -> None:
        if self.width != None:
            if self.width < 0:
                self.width = 0
                raise ValueError("Oh no width < 0")
        self.size = (self.width, self.height)
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        #self.overlay_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        if self.width != None:
            if self.width < 0:
                Logger.warning(f"Overlay: Oh no width = {self.width} < 0")
                self.width = 0
                #raise ValueError("Oh no width < 0")
        
        self.size = list(screen.get_size())
        if self.width != None:
            self.size[0] = self.width
        if self.height != None:
            self.size[1] = self.height
        self.size = tuple(self.size)

        #print(f"Overlay: size = {self.size}")
        
        if self.size != self.prev_size:
            self.overlay_surface = pg.Surface(self.size, pg.SRCALPHA)
            self.overlay_surface.fill(self.color_alpha)
        self.prev_size = self.size
        
        #pg.draw.polygon(self.overlay_surface, (0, 255, 0), [(20, 80), (80, 80), (50, 20)])
        screen.blit(self.overlay_surface, self.pos)