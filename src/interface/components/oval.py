from __future__ import annotations
import pygame as pg

from src.utils import GameSettings
from src.core.services import input_manager, sound_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
from .whshape import WHShape, Shape

class Oval(WHShape):
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
    
    # Outer frame
    draw_outer_frame: bool
    outer_frame_color: tuple[int, int, int]
    outer_frame_width: int
    
    def __init__(
        self,
        color: tuple[int, int, int],
        x: int, y: int,
        width: int, height: int,
        can_drag: bool = False,
        draw_outer_frame: bool = False,
        outer_frame_color: tuple[int, int, int] = (255, 255, 255),
        outer_frame_width: int = 3
    ):
        """
        Draws an oval
        (x, y) is center
        """
        super().__init__(color, x, y, width, height, can_drag)
        
        # Outer frame
        self.draw_outer_frame = draw_outer_frame
        self.outer_frame_color = outer_frame_color
        self.outer_frame_width = 3
    
    @override
    def update(self, dt: float) -> None:
        super().update(dt)
    
    @override
    def draw_to_surface(self):
        #pg.draw.ellipse(self.surface, self.color, (0, 0, self.width, self.height))
        self.draw_shape(Shape.Oval)
        if self.draw_outer_frame:
            pg.draw.ellipse(self.surface, self.outer_frame_color, (0, 0, self.width, self.height), self.outer_frame_width)
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        super().draw(screen)
        