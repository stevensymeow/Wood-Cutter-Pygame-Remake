from __future__ import annotations
import pygame as pg

from src.utils import GameSettings
from src.core.services import input_manager, sound_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
from enum import Enum

class Shape(Enum):
    Nothing = 0
    Rectangle = 1
    Oval = 2

class WHShape(UIComponent):
    # Pos and Size
    color: tuple[int, int, int]
    x: int
    y: int
    pos_x: int
    pos_y: int
    width: int
    height: int
    pos_size: tuple[int, int, int, int]
    hitbox: pg.Rect
    
    # Surface
    surface: pg.Surface
    
    # Drag
    can_drag: bool
    dragging: bool
    drag_dx: int
    drag_dy: int
    
    # Rotate
    degree: float
    angle: float
    
    def __init__(
        self,
        color: tuple[int, int, int],
        x: int, y: int,
        width: int, height: int,
        can_drag: bool = False
    ):
        """
        Draws an shape of width and height
        (x, y) is center
        """
        self.color = color
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pos_x = self.x - self.width / 2
        self.pos_y = self.y - self.height / 2
        self.pos_size = (self.pos_x, self.pos_y, self.width, self.height)
        self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        #self.hitbox = pg.Rect(*self.pos_size)
        self.hitbox = self.surface.get_rect()
        
        # Rotate
        self.angle = 0
        self.degree = 0
        
        # Drag
        self.can_drag = can_drag
        self.dragging = False
        self.drag_dx = 0
        self.drag_dy = 0
    
    def set_width(self, width: int):
        self.width = width
        self.pos_x = self.x - self.width / 2
        
    def set_height(self, height: int):
        self.height = height
        self.pos_y = self.y - self.height / 2
    
    def set_color(self, color: tuple[int, int, int]):
        self.color = color
    
    def move_by(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
        self.pos_x += dx
        self.pos_y += dy
    
    def set_pos(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.pos_x = self.x - self.width / 2
        self.pos_y = self.y - self.height / 2
    
    def rotate(self, degree: float = 2):
        self.degree = degree
    
    def set_angle(self, angle: float = 0):
        self.angle = angle % 360
    
    def do_rotate(self):
        self.angle = (self.angle + self.degree) % 360
        self.surface = pg.transform.rotozoom(self.surface, self.angle, 1)
        self.hitbox = self.surface.get_rect()
        self.hitbox.center = (self.pos_x + self.width/2, self.pos_y + self.height/2)
        self.degree = 0
    
    def draw_shape(self, shape: Shape = Shape.Nothing):
        match (shape):
            case Shape.Rectangle:
                pg.draw.rect(self.surface, self.color, (0, 0, self.width, self.height))
            case Shape.Oval:
                pg.draw.ellipse(self.surface, self.color, (0, 0, self.width, self.height))
    
    def draw_to_surface(self):
        self.draw_shape()
    
    @override
    def update(self, dt: float) -> None:
        if self.width < 0:
            self.width = 0
            raise ValueError("Oh no width < 0")
        if self.height < 0:
            self.height = 0
            raise ValueError("Oh no height < 0")
        
        self.pos_size = (self.pos_x, self.pos_y, self.width, self.height)
        self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        
        self.draw_to_surface()
        
        #self.hitbox = pg.Rect(*self.pos_size)
        self.do_rotate()
        
        # Drag
        if self.can_drag:
            if input_manager.mouse_pressed(1):
                if self.hitbox.collidepoint(input_manager.mouse_pos):
                    if not self.dragging:
                        self.drag_dx = self.x - input_manager.mouse_pos[0]
                        self.drag_dy = self.y - input_manager.mouse_pos[1]
                    self.dragging = True
            elif input_manager.mouse_released(1):
                self.dragging = False
            
            if self.dragging:
                mouse_x, mouse_y = input_manager.mouse_pos
                self.set_pos(mouse_x + self.drag_dx, mouse_y + self.drag_dy)
                
            if input_manager.mouse_pressed(3) and self.hitbox.collidepoint(input_manager.mouse_pos):
                pcx, pcy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT / 2
                Logger.info(f"{self.__class__.__name__}: (x, y) = {self.x, self.pos_y}, {self.x - pcx, self.y - pcy} \t {pcx, pcy}")
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.hitbox.topleft)
        