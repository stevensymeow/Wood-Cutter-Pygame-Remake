from __future__ import annotations
import pygame as pg

#from src.sprites import Sprite
from src.core.services import input_manager, sound_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
from src.interface.components import Text, Overlay, Oval

class OvalButton(UIComponent):
    oval_button: Oval
    color: tuple[int, int, int]
    hitbox: pg.Rect
    on_click: Callable[[], None] | None

    x: int
    y: int
    pos_x: int
    pos_y: int
    width: int
    height: int
    
    # Text
    text_str: str
    text_size: int
    text_font: str
    text_color: tuple[int]
    text_width: str
    button_text: Text
    text_x: int
    text_y: int
    
    # Hover
    can_hover: bool
    is_drawn: bool
    moving: bool
    
    # Overlay
    dark_overlay: Overlay
    
    # Hover Text
    hover_text_str: str
    hover_text_size: int
    hover_text_font: str
    hover_text_color: tuple[int]
    hover_text_color_alpha: tuple[int]
    hover_text_width: str
    hover_text: Text
    hover_text_x: int
    hover_text_y: int
    hovered: bool
    
    # Hover pop
    just_hovered: bool

    def __init__(
        self,
        color: tuple[int, int, int],
        x: int, y: int, width: int, height: int,
        on_click: Callable[[], None] | None = None, 
        text_str: str = "", text_size: int = 10, text_font: str = "Minecraft.ttf", text_color: tuple[int] = (0, 0, 0), text_pos: int = 0,
        hover_text_str: str = "", hover_text_size: int = 10, hover_text_font: str = "Minecraft.ttf",
        hover_text_color: tuple[int] = (255, 255, 255), hover_text_color_alpha: tuple[int] = (50, 50, 50, 255),
        can_hover: bool = True
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.color = color
        self.oval_button = Oval(self.color, x, y, width, height)
        self.hitbox = self.oval_button.hitbox
        self.on_click = on_click
        self.pos_x = self.oval_button.pos_x
        self.pos_y = self.oval_button.pos_y

        # Text
        self.text_str = text_str
        self.text_size = text_size
        self.text_font = text_font
        self.text_color = text_color
        self.button_text = Text(self.text_str, self.text_size, self.text_font, self.text_color, x, y)
        self.text_width = self.button_text.get_width()
        self.text_x = self.pos_x + (self.width - self.text_width)/2
        self.text_y = self.pos_y + (self.height - self.text_size)/2
        self.text_pos = text_pos
        match (self.text_pos):
            case 0:
                self.text_y = self.pos_y + (self.height - self.text_size)/2
            case 1:
                self.text_y = self.pos_y - self.text_size
            case 2:
                self.text_y = self.pos_y + self.height
        self.button_text.set_pos(self.text_x, self.text_y)
        
        # Hover Text
        self.hover_text_str = hover_text_str
        if hover_text_str:
            self.hover_text_str = f" {hover_text_str} "
        self.hover_text_size = hover_text_size
        self.hover_text_font = hover_text_font
        self.hover_text_color = hover_text_color
        self.hover_text_color_alpha = hover_text_color_alpha
        self.hover_text = Text(self.hover_text_str, self.hover_text_size, self.hover_text_font, self.hover_text_color, x, y, self.hover_text_color_alpha)
        self.hover_text_width = self.hover_text.get_width()
        self.hover_text_x = self.pos_x - self.hover_text_width
        self.hover_text_y = self.pos_y
        self.hover_text.set_pos(self.hover_text_x, self.hover_text_y)
        self.hovered = False
        self.just_hovered = False
        
        # Overlay
        self.dark_overlay = Overlay((0, 0, 0, 100), (self.pos_x, self.pos_y), self.width, self.height)
        
        # Hover
        self.can_hover = can_hover
        self.is_drawn = False
        self.moving = False

    def set_all(
        self,
        color: tuple[int, int, int],
        x: int, y: int, width: int, height: int,
        on_click: Callable[[], None] | None = None, 
        text_str: str = "", text_size: int = 10, text_font: str = "Minecraft.ttf", text_color: tuple[int] = (0, 0, 0),
        hover_text_str: str = "", hover_text_size: int = 10, hover_text_font: str = "Minecraft.ttf",
        hover_text_color: tuple[int] = (255, 255, 255), hover_text_color_alpha: tuple[int] = (50, 50, 50, 255),
        can_hover: bool = True
    ):
        self.pos_x = x
        self.pos_y = y
        self.width = width
        self.height = height
        
        self.color = color
        self.oval_button = Oval(self.color, x, y, width, height)
        self.hitbox = self.oval_button.hitbox
        self.on_click = on_click

        # Text
        self.text_str = text_str
        self.text_size = text_size
        self.text_font = text_font
        self.text_color = text_color
        self.button_text = Text(self.text_font, self.text_size, self.text_str, self.text_color, x, y)
        self.text_width = self.button_text.get_width()
        self.text_x = self.pos_x + (self.width - self.text_width)/2
        self.text_y = self.pos_y + (self.height - self.text_size)/2
        self.button_text.set_pos(self.text_x, self.text_y)
        
        # Hover Text
        self.hover_text_str = hover_text_str
        if hover_text_str:
            self.hover_text_str = f" {hover_text_str} "
        #if self.hover_text_str:
            #print(self.hover_text_str)
        self.hover_text_size = hover_text_size
        self.hover_text_font = hover_text_font
        self.hover_text_color = hover_text_color
        self.hover_text_color_alpha = hover_text_color_alpha
        self.hover_text = Text(self.hover_text_font, self.hover_text_size, self.hover_text_str, self.hover_text_color, x, y, self.hover_text_color_alpha)
        self.hover_text_width = self.hover_text.get_width()
        self.hover_text_x = self.pos_x
        self.hover_text_y = self.pos_y
        self.hover_text.set_pos(self.hover_text_x, self.hover_text_y)
        self.hovered = False
        self.just_hovered = False
        
        # Hover
        self.can_hover = can_hover
    
    @override
    def update(self, dt: float, can_be_hovered: bool = True) -> None:
        # Hover alpha
        if self.can_hover:
            self.oval_button.set_alpha(255)
        else:
            self.oval_button.set_alpha(200)
            
        # Oval
        self.oval_button.update(dt)
        self.hitbox = self.oval_button.hitbox
        
        if self.hitbox.collidepoint(input_manager.mouse_pos) and self.is_drawn and not(self.moving) and self.can_hover:
            self.hovered = True
            
            # Hover pop
            if not self.just_hovered:
                self.just_hovered = True
                sound_manager.play_sound("pop.wav")
            
            # Hover Text follow mouse position
            if self.hover_text_str:
                self.hover_text_x = input_manager.mouse_pos[0] - self.hover_text_width
                self.hover_text_y = input_manager.mouse_pos[1] - self.hover_text_size
                self.hover_text.set_pos(self.hover_text_x, self.hover_text_y)
            
            if input_manager.mouse_pressed(1) and self.on_click is not None and self.can_hover and can_be_hovered:
                self.on_click()
        else:
            self.hovered = False
            self.just_hovered = False
        self.is_drawn = False
        self.moving = False

        
        # Text
        if self.text_str:
            self.button_text.update(dt)
            
        # Hover
        if self.hover_text_str:
            self.hover_text.update(dt)
        
        # Overlay
        self.dark_overlay.update(dt)
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        # Oval
        self.oval_button.draw(screen)
        if self.hovered:
            self.oval_button.draw_outer_frame = True
            #pg.draw.rect(screen, (255, 255, 255), self.hitbox, 1)
        else:
            self.oval_button.draw_outer_frame = False

        # Text
        if self.text_str:
            self.button_text.draw(screen)
            
        # Hover
        """
        if not(self.can_hover):
            self.dark_overlay.draw(screen)
        """
        
        # Hover Text
        if self.hover_text_str:
            if self.hovered:
                self.hover_text.draw(screen)
        
        # Hover
        self.is_drawn = True
    
    def move_by(self, dx: int, dy: int):
        self.pos_x += dx
        self.pos_y += dy
        self.oval_button.move_by(dx, dy)
        self.button_text.move_by(dx, dy)
        self.dark_overlay.move_by(dx, dy)
        
        # Hover
        self.hitbox = self.oval_button.hitbox
        self.moving = True

    def set_pos(self, x: int, y: int):
        self.x, self.y = x, y
        self.oval_button.set_pos(x, y)
        self.pos_x = self.oval_button.pos_x
        self.pos_y = self.oval_button.pos_y
        self.text_x = self.pos_x + (self.width - self.text_width)/2
        self.text_y = self.pos_y + (self.height - self.text_size)/2
        match (self.text_pos):
            case 0:
                self.text_y = self.pos_y + (self.height - self.text_size)/2
            case 1:
                self.text_y = self.pos_y - self.text_size
            case 2:
                self.text_y = self.pos_y + self.height
        self.button_text.set_pos(self.text_x, self.text_y)
        self.dark_overlay.set_pos(x, y)
        
        # Hover
        self.hitbox = self.oval_button.hitbox
    
    # Set hover text
    def set_hover_text(self, text_str: str):
        self.hover_text_str = text_str
        self.hover_text.set_text(f" {text_str} ")
        dt = 0 # doesn't matter
        self.hover_text.update(dt)
        self.hover_text_width = self.hover_text.get_width()

    # Set color
    def set_color(self, color: tuple[int, int, int]):
        self.oval_button.set_color(color)
