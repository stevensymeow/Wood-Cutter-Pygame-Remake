from __future__ import annotations
import pygame as pg

from src.utils import GameSettings
from src.core.services import input_manager, sound_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
from .whshape import WHShape, Shape

class Rectangle(WHShape):
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
    
    # Drag
    can_drag: bool
    dragging: bool
    drag_dx: int
    drag_dy: int
    
    def __init__(
        self,
        color: tuple[int, int, int],
        x: int, y: int,
        width: int, height: int,
        can_drag: bool = False
    ):
        """
        Draws an rectangle
        (x, y) is center
        """
        super().__init__(color, x, y, width, height, can_drag)
    
    @override
    def update(self, dt: float) -> None:
        super().update(dt)
    
    @override
    def draw_to_surface(self):
        #pg.draw.rect(self.surface, self.color, (0, 0, self.width, self.height))
        self.draw_shape(Shape.Rectangle)
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        super().draw(screen)
