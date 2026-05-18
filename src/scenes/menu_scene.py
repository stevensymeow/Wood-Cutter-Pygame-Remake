import pygame as pg

from src.utils import GameSettings
from src.scenes.scene import Scene
from src.interface.components import Text, Overlay, Oval, Rectangle, OvalButton
from src.core.services import scene_manager, sound_manager, input_manager
from typing import override

class MenuScene(Scene):
    # Background
    background: Overlay
    
    # Buttons
    
    # Title
    main_title: Text
    
    def __init__(self):
        super().__init__()
        # Background
        self.background = Overlay((0, 255, 255, 255))
        
        # Title
        ux, uy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT * 1 / 4
        self.main_title = Text("Wood Cutter", 64, "Pokemon Solid.ttf", (255, 0, 0), ux, uy - 30)
        self.main_title.move_by(-self.main_title.get_width()/2, 0)
        
        # Trees
        pcx, pcy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT / 2
        hy = GameSettings.SCREEN_HEIGHT
        self.rectangle_1 = Rectangle((204, 122, 0), pcx-320, hy-100, 45, 200)
        self.oval_1 = Oval((0, 200, 83), pcx-320, hy-100-80, 120, 160)
        self.rectangle_2 = Rectangle((204, 122, 0), pcx+320, hy-100, 45, 200)
        self.oval_2 = Oval((0, 200, 83), pcx+320, hy-100-80, 120, 160)
        self.out = True
        self.dx = 0
        
        # Button
        self.start_button = OvalButton((255, 125, 0), pcx, pcy+100, 180, 60,
                                       on_click=lambda: scene_manager.change_scene("game"),
                                       text_str="START", text_size=30, text_color=(255, 255, 255))
        
    @override
    def enter(self) -> None:
        sound_manager.play_bgm("xylo1.wav")
        self.rectangle_1.set_angle()
        self.oval_1.set_angle()
        self.rectangle_2.set_angle()
        self.oval_2.set_angle()
    
    @override
    def exit(self) -> None:
        sound_manager.stop_all_sounds()
        sound_manager.play_sound("Meow2.wav")
    
    @override
    def update(self, dt: float):
        # Title
        self.main_title.update(dt)
        
        # Trees
        pcx, pcy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT / 2
        
        movement = 1
        if self.out:
            if self.dx <= 10:
                self.dx += movement
                self.rectangle_1.move_by(-movement, 0)
                self.oval_1.move_by(-movement, 0)
                self.rectangle_2.move_by(movement, 0)
                self.oval_2.move_by(movement, 0)
            else:
                self.out = False
        else:
            if self.dx >= -10:
                self.dx -= 1
                self.rectangle_1.move_by(movement, 0)
                self.oval_1.move_by(movement, 0)
                self.rectangle_2.move_by(-movement, 0)
                self.oval_2.move_by(-movement, 0)
            else:
                self.out = True
            
        if input_manager.key_down(pg.K_1):
            self.rectangle_1.rotate(10)
            self.rectangle_2.rotate(-10)
        if input_manager.key_down(pg.K_2):
            self.oval_1.rotate(10)
            self.oval_2.rotate(-10)
        self.rectangle_1.update(dt)
        self.oval_1.update(dt)
        self.rectangle_2.update(dt)
        self.oval_2.update(dt)
        
        # Button
        self.start_button.update(dt)
        
    @override
    def draw(self, screen: pg.Surface):
        # Background
        self.background.draw(screen)
        
        # Title
        self.main_title.draw(screen)
        
        # Trees
        self.rectangle_1.draw(screen)
        self.oval_1.draw(screen)
        self.rectangle_2.draw(screen)
        self.oval_2.draw(screen)
        
        # Button
        self.start_button.draw(screen)
        
        