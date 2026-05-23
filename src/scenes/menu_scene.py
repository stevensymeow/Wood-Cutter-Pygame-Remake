import pygame as pg

from src.data.info import GameInfo
from src.utils import GameSettings, Logger
from src.scenes.scene import Scene
from src.interface.components import Text, Overlay, Oval, Rectangle, OvalButton
from src.core.services import scene_manager, sound_manager, input_manager
from src.core import GameManager
from typing import override

class MenuScene(Scene):
    # Background
    background: Overlay
    
    # Game Manager
    game_manager: GameManager
    
    # Buttons
    start_button: OvalButton
    
    # Title
    main_title: Text
    
    def __init__(self):
        super().__init__()
        
        # Game Manager
        self.game_manager = scene_manager.game_manager
        
        # Background
        self.background = Overlay()
        background_color = self.game_manager.curr_lv.background_color
        self.background.set_color(background_color)
        
        # Title
        ux, uy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT * 1 / 4
        title_color = self.game_manager.curr_lv.title_color
        self.main_title = Text("Wood Cutter", 64, "Pokemon Solid.ttf", title_color, ux, uy - 30)
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
        button_color = self.game_manager.curr_lv.button_color
        self.start_button = OvalButton(button_color, pcx, pcy+100, 180, 60,
                                       on_click=lambda: scene_manager.change_scene("game"),
                                       text_str="START", text_size=30, text_color=(255, 255, 255))
        self.nlevel_button = OvalButton(button_color, pcx, pcy+100+10+60, 180, 60,
                                       on_click=lambda: self.switch_level(1),
                                       text_str="Next Level", text_size=20, text_color=(255, 255, 255))
        self.plevel_button = OvalButton(button_color, pcx, pcy+100+10+60+10+60, 180, 60,
                                       on_click=lambda: self.switch_level(-1),
                                       text_str="Previous Level", text_size=20, text_color=(255, 255, 255))

    @override
    def enter(self) -> None:
        sound_manager.play_bgm(self.game_manager.curr_lv.bgm_path)
        #sound_manager.play_bgm("Punch.wav")
        #sound_manager.play_bgm("strongpunch.wav")
        # Tree
        self.rectangle_1.set_angle()
        self.oval_1.set_angle()
        self.rectangle_2.set_angle()
        self.oval_2.set_angle()
    
    @override
    def exit(self) -> None:
        sound_manager.stop_all_sounds()
        sound_manager.play_sound("Meow2.wav")
        # Tree
        self.rectangle_1.set_angle()
        self.oval_1.set_angle()
        self.rectangle_2.set_angle()
        self.oval_2.set_angle()
    
    # Switch level
    def switch_level(self, switch: int = 1):
        switched = False
        if switch > 0:
            switched = GameInfo.to_next_level()
        else:
            switched = GameInfo.to_prev_level()
        if switched:
            curr_lv = self.game_manager.curr_lv
            Logger.info(f"Current level: {curr_lv.level_label} {curr_lv.level_name}")
            # BGM
            sound_manager.play_bgm(curr_lv.bgm_path)
            # Background
            self.background.set_color(curr_lv.background_color)
            # Title text
            self.main_title.set_color(curr_lv.title_color)
            # Buttons
            button_color = curr_lv.button_color
            self.start_button.set_color(button_color)
            self.nlevel_button.set_color(button_color)
            self.plevel_button.set_color(button_color)
            # Tree
            self.rectangle_1.set_angle()
            self.oval_1.set_angle()
            self.rectangle_2.set_angle()
            self.oval_2.set_angle()
    
    @override
    def update(self, dt: float):
        # Background
        self.background.update(dt)
        
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
        
        # -- Button --
        self.start_button.update(dt)
        # Level
        self.nlevel_button.can_hover = self.game_manager.has_next_level
        self.plevel_button.can_hover = self.game_manager.has_prev_level
        self.nlevel_button.update(dt)
        self.plevel_button.update(dt)
        
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
        self.nlevel_button.draw(screen)
        self.plevel_button.draw(screen)
        