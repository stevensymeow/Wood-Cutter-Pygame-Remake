from __future__ import annotations
import pygame as pg

from src.core.services import input_manager, sound_manager, resource_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent

class Text(UIComponent):
    text_font: pg.font.Font
    text_surface: pg.Surface
    text_size: int
    text_display: str
    color: tuple[int]
    pos_x: int
    pos_y: int
    # max width
    max_width: int
    # cursor index
    cursor_index: int
    
    def __init__(
        self,
        text_display: str, text_size: int, font_path: str, color: tuple[int],
        x: int, y: int,
        color_alpha: tuple[int] = None, max_width: int = 0
    ):
        self.text_font = resource_manager.get_font(font_path, text_size)
        self.pos_x, self.pos_y = x, y
        self.text_size = text_size
        self.text_display = text_display
        self.color = color
        self.text_surface = self.text_font.render(self.text_display, True, self.color)
        # Back
        self.color_alpha = color_alpha
        self.back_surface = self.text_font.render(self.text_display, True, self.color)
        if self.color_alpha:
            self.back_surface.fill(self.color_alpha)
            
        # max width
        self.text_width = self.get_width()
        self.max_width = max_width
        
        # cursor index
        self.cursor_index = 0
        self.cursor_index = len(self.text_display)
        
    @override
    def update(self, dt: float) -> None:
        self.text_surface = self.text_font.render(self.text_display, True, self.color)
        # Back
        if self.color_alpha:
            self.back_surface = self.text_font.render(self.text_display, True, self.color)
            self.back_surface.fill(self.color_alpha)
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        # Back
        if self.color_alpha:
            screen.blit(self.back_surface, (self.pos_x, self.pos_y))
        
        screen.blit(self.text_surface, (self.pos_x, self.pos_y))

    def set_color(self, color: tuple[int, int, int]):
        self.color = color
    
    def get_width(self):
        return self.text_surface.get_width()

    def set_text(self, text_display: str):
        self.text_display = text_display
        self.cursor_index = len(self.text_display)
        
    def add_words(self, words: str):
        if words == "":
            return
        
        # max width
        if self.max_width > 0 and self.get_width() < self.max_width:
            # cursor index
            #print(self.cursor_index)
            if self.cursor_index == len(self.text_display):
                self.text_display += words
                self.cursor_index += len(words)
            elif 0 <= self.cursor_index < len(self.text_display):
                self.text_display = self.text_display[:self.cursor_index] + words + self.text_display[self.cursor_index:]
                self.cursor_index += len(words)
    
    def del_by_letter(self):
        lenth = len(self.text_display)
        if lenth > 0:
            if self.cursor_index == len(self.text_display):
                self.text_display = self.text_display[:lenth-1]
                # cursor index
                if self.cursor_index > 0:
                    self.cursor_index -= 1
            elif 0 < self.cursor_index < len(self.text_display):
                self.text_display = self.text_display[:self.cursor_index-1] + self.text_display[self.cursor_index:]
                # cursor index
                if self.cursor_index > 0:
                    self.cursor_index -= 1
    
    # cursor index
    def set_cursor_index(self, index: int):
        if 0 <= index <= len(self.text_display):
            self.cursor_index = index
    def get_cursor_index(self) -> int:
        return self.cursor_index
    # get width by cursor index
    def get_width_by_cursor_index(self) -> int:
        if self.cursor_index > 0:
            if self.cursor_index < len(self.text_display):
                return self.text_font.render(self.text_display[:self.cursor_index], True, self.color).get_width()
            else:
                return self.get_width()
        else:
            return 0
    
    def clear_str(self) -> str:
        text_display = self.text_display
        self.text_display = ""
        # cursor index
        self.cursor_index = 0
        return text_display
        
    def set_pos(self, x: int, y: int):
        self.pos_x, self.pos_y = x, y
        
    def move_by(self, dx: int, dy: int):
        self.pos_x += dx
        self.pos_y += dy
        
    