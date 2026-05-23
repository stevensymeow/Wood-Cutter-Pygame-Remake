import pygame as pg

from src.data.info import GameInfo
from src.utils import GameSettings, Logger
from src.scenes.scene import Scene
from src.interface.components import Text, Overlay, Oval, Rectangle, OvalButton, RunningText, WoodCutter, Branch
from src.core.services import scene_manager, sound_manager, input_manager
from src.core import GameManager, Game
from typing import override

class GameScene(Scene):
    # Background
    background: Overlay
    
    # Game Manager
    game_manager: GameManager
    
    # Buttons
    back_button: OvalButton
    retry_button: OvalButton
    
    # Text
    high_score_text: Text
    gem_text: Text
    branch_text: Text
    score_text: Text
    
    def __init__(self):
        super().__init__()
        
        # Game Manager
        self.game_manager = GameManager.make(input_manager, sound_manager)
        
        # Background
        self.background = Overlay()
        background_color = self.game_manager.curr_lv.background_color
        self.background.set_color(background_color)
        
        # Tree Bark
        pcx, pcy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT / 2
        hy = GameSettings.SCREEN_HEIGHT
        #self.tree_bark = Rectangle((204, 122, 0), pcx, pcy, 80, hy)
        
        # Running Text
        font = GameSettings.TEXT_FONT
        run_text = "As you can see, this is the classic Poper-cop313 Wood Cutter game REMAKE!!!"
        self.running_text = RunningText(run_text, 20, font, (0, 0, 255))
        
        # Buttons
        wx, hy = GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT
        button_color = self.game_manager.curr_lv.button_color
        self.back_button = OvalButton(button_color, wx-90-20, hy-60-20, 60, 60,
                                      on_click=lambda: scene_manager.change_scene("menu"),
                                      text_str="BACK", text_size=15, text_color=(255, 255, 255))
        self.retry_button = OvalButton(button_color, 90+20, hy-60-20, 60, 60,
                                      on_click=lambda: self.game_manager.retry(),
                                      text_str="RETRY", text_size=15, text_color=(255, 255, 255))

        # Text
        wx, hy = GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT
        font = GameSettings.TEXT_FONT
        text_size = 24
        text_color = self.game_manager.curr_lv.score_color
        self.high_score_text = Text(f"Highest Score: {self.game_manager.highest_score}", text_size, font, text_color,
                                    20, 20+10)
        spaces = 200
        self.gem_text = Text(f"Gems: {self.game_manager.collected_gems}", text_size, font, text_color,
                             wx-spaces, 20+10)
        self.branch_text = Text(f"Branches: {self.game_manager.fallen_branches}", text_size, font, text_color,
                             wx-spaces, 20+10+text_size+10)
        self.score_text = Text(f"Score: {self.game_manager.score}", text_size, font, text_color,
                             wx-spaces, 20+10+text_size+10+text_size+10)
    
    @override
    def enter(self) -> None:
        # Game manager
        self.game_manager.enter()
        
        # Running Text
        self.running_text.pos_init()
        
        # -- Level --
        curr_lv = self.game_manager.curr_lv
        # Background
        self.background.set_color(curr_lv.background_color)
        # Buttons
        button_color = curr_lv.button_color
        self.back_button.set_color(button_color)
        self.retry_button.set_color(button_color)
        # Score Text
        score_color = curr_lv.score_color
        self.high_score_text.set_color(score_color)
        self.gem_text.set_color(score_color)
        self.branch_text.set_color(score_color)
        self.score_text.set_color(score_color)
    
    @override
    def exit(self) -> None:
        # Sound
        sound_manager.stop_all_sounds()
        sound_manager.play_sound("Meow.wav")
        
        # Game manager
        self.game_manager.exit()
        
        # Running Text
        self.running_text.pos_init()
    
    @override
    def update(self, dt: float):
        # Game manager
        self.game_manager.update(dt)
        
        # Back
        if self.game_manager.state != Game.Playing:
            if input_manager.key_pressed(pg.K_b):
                scene_manager.change_scene("menu")
        
        # Background
        self.background.update(dt)
        
        # Running Text
        self.running_text.update(dt)
        
        # Buttons
        if self.game_manager.state != Game.Playing:
            self.back_button.update(dt)
        if self.game_manager.state == Game.GG:
            self.retry_button.update(dt)
        
        # Text
        self.high_score_text.set_text(f"Highest Score: {self.game_manager.highest_score}")
        self.high_score_text.update(dt)
        self.gem_text.set_text(f"Gems: {self.game_manager.collected_gems}")
        self.gem_text.update(dt)
        self.branch_text.set_text(f"Branches: {self.game_manager.fallen_branches}")
        self.branch_text.update(dt)
        self.score_text.set_text(f"Score: {self.game_manager.score}")
        self.score_text.update(dt)
    
    @override
    def draw(self, screen: pg.Surface):
        # Background
        self.background.draw(screen)
        
        # Game components
        self.game_manager.draw_components(screen)
        
        # Buttons
        if self.game_manager.state != Game.Playing:
            self.back_button.draw(screen)
        if self.game_manager.state == Game.GG:
            self.retry_button.draw(screen)
        
        # Text
        self.high_score_text.draw(screen)
        self.gem_text.draw(screen)
        self.branch_text.draw(screen)
        self.score_text.draw(screen)

        # Running Text
        self.running_text.draw(screen)