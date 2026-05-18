import pygame as pg

from src.utils import GameSettings

class OverlayScene():
    overlay_surface: pg.Surface
    color: tuple[int, int, int]
    alpha: int
    color_alpha: tuple[int, int, int, int]
    pos: tuple[int, int]
    pos_x: int
    pos_y: int
    size: tuple[int, int]
    
    def __init__(
        self,
        color: tuple[int, int, int] = (0, 0, 0),
        alpha: int = 255
    ):
        self.pos = (0, 0)
        self.pos_x, self.pos_y = self.pos
        
        self.color = color
        self.alpha = alpha
        self.color_alpha = self.color + (self.alpha, )
        
        self.size = (0, 0)
        
        self.overlay_surface = pg.Surface(self.size, pg.SRCALPHA)
    
    def set_color(self, color: tuple[int, int, int]):
        if color != self.color:
            self.color = color
            self.color_alpha = self.color + (self.alpha, )

    def set_alpha(self, alpha: int = 255):
        if alpha < 0: alpha = 0
        if alpha > 255: alpha = 255
        if alpha != self.alpha:
            self.alpha = alpha
            self.color_alpha = self.color + (self.alpha, )
    
    def change_alpha(self, dalpha: int):
        self.alpha += dalpha
        if self.alpha < 0: self.alpha = 0
        if self.alpha > 255: self.alpha = 255
        self.color_alpha = self.color + (self.alpha, )
    
    def draw(self, screen: pg.Surface) -> None:
        self.size = screen.get_size()
        self.overlay_surface = pg.Surface(self.size, pg.SRCALPHA)
        self.overlay_surface.fill(self.color_alpha)
        screen.blit(self.overlay_surface, self.pos)
        