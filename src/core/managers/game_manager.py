from __future__ import annotations
from src.utils import Logger, GameSettings
import pygame as pg
from enum import Enum
import random
import math
from typing import Callable
from typing import TYPE_CHECKING
from src.data.info import GameInfo

if TYPE_CHECKING:
    from src.core.managers import InputManager, SoundManager, SceneManager
    from src.interface.components import OvalButton, WoodCutter, Branch, Gem, Rectangle

class Game(Enum):
    Init = -1
    Entered = 0
    Playing = 1
    Paused = 2
    GG = 3

class GameManager:
    # Managers
    input_manager: InputManager
    sound_manager: SoundManager
    
    # State
    state: Game
    
    # Score
    highest_score: int
    collected_gems: int
    fallen_branches: int
    score: int
    
    # --- Components ---
    # Tree Bark
    tree_bark: Rectangle
    
    # Wood Cutter
    wood_cutter: WoodCutter
    
    # -- Branches --
    branches: list[Branch]
    make_new_branch: Callable[[int], Branch]
    
    # -- Gems --
    gems: list[Branch]
    make_new_gem: Callable[[int], Gem]
    
    def __init__(self, input_manager: InputManager, sound_manager: SoundManager):
        # Managers
        self.input_manager = input_manager
        self.sound_manager = sound_manager
        
        # State
        self.state = Game.Init
        
        # Score
        self.highest_score = 0
        self.collected_gems = 0
        self.fallen_branches = 0
        self.score = 0
        
        # --- Components ---
        # Branches
        self.branches = []
        
        # Gems
        self.gems = []
    
    @classmethod
    def make(cls, input_manager: InputManager, sound_manager: SoundManager) -> "GameManager":
        from src.interface.components import OvalButton, WoodCutter, Branch, Gem, Rectangle
        from src.core.services import scene_manager
        
        gm = cls(input_manager, sound_manager)
        
        # --- Components ---
        # Tree Bark
        pcx, pcy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT / 2
        hy = GameSettings.SCREEN_HEIGHT
        gm.tree_bark = Rectangle((204, 122, 0), pcx, pcy, GameInfo.bark_width, hy)
        
        # Wood Cutter
        gm.wood_cutter = WoodCutter(gm)
        
        # -- Branches --
        gm.branches = []
        
        def new_branch(pos: int = -1) -> Branch:
            return Branch(gm, pos=pos)
        gm.make_new_branch = new_branch
        
        # -- Gems --
        gm.gems = []
        
        def new_gem(pos: int = -1) -> Gem:
            return Gem(gm, pos=pos)
        gm.make_new_gem = new_gem
        
        return gm

    # -- Branches --
    def add_new_branch(self, count: int = 1):
        for _ in range(count):
            pos = random.randint(0, 1)*2 - 1
            #Logger.info(f"pos: {pos}")
            self.branches.append(self.make_new_branch(pos))
    
    def del_first_branch(self):
        self.branches.pop(0)
    
    def del_all_branches(self):
        self.branches.clear()
    # -- Branches --
    
    # -- Gems --
    def add_new_gem(self, count: int = 1):
        for _ in range(count):
            pos = random.randint(0, 1)*2 - 1
            #Logger.info(f"pos: {pos}")
            self.gems.append(self.make_new_gem(pos))
    
    def del_first_gem(self):
        self.gems.pop(0)
    
    def del_all_gems(self):
        self.gems.clear()
    # -- Gems --
    
    def enter(self) -> None:
        self.state = Game.Entered
        self.game_init()
    
    def exit(self) -> None:
        self.state = Game.Entered
        self.game_init()
    
    def game_init(self):
        # Score
        #self.highest_score = 0
        self.collected_gems = 0
        self.fallen_branches = 0
        self.score = 0
        
        # --- Components ---
        self.wood_cutter.pos_init()
        
        # -- Branches --
        self.del_all_branches()
        
        # -- Gems --
        self.del_all_gems()
    
    # Retry
    def retry(self):
        self.state = Game.Entered
        self.sound_manager.stop_all_sounds()
        self.game_init()
    
    def update(self, dt: float) -> None:
        # State
        match (self.state):
            case Game.Entered:
                left_bound = self.wood_cutter.x_left - self.wood_cutter.width/2
                right_bound = self.wood_cutter.x_right + self.wood_cutter.width/2
                start_condition = self.input_manager.key_pressed(pg.K_LEFT) or self.input_manager.key_pressed(pg.K_RIGHT) or \
                    (self.input_manager.mouse_pressed(1) and left_bound <= self.input_manager.mouse_pos[0] <= right_bound)
                if start_condition:
                    self.game_init()
                    self.state = Game.Playing
                    self.sound_manager.play_bgm("xylo1.wav")
                    #self.sound_manager.play_bgm("dance celebrate.wav")
                    self.add_new_branch()
                    #self.add_new_gem()
            case Game.Playing:
                # Pause
                if self.input_manager.key_pressed(pg.K_SPACE):
                    self.state = Game.Paused
                    self.sound_manager.pause_all()
                # Score
                self.score = self.collected_gems + self.fallen_branches
                if self.score > self.highest_score:
                    self.highest_score = self.score
            case Game.Paused:
                # Resume
                if self.input_manager.key_pressed(pg.K_SPACE):
                    self.state = Game.Playing
                    self.sound_manager.resume_all()
            case Game.GG:
                self.sound_manager.stop_bgm()
                # Retry
                if self.input_manager.key_pressed(pg.K_r):
                    self.retry()
        
        # Hitbox debug
        if self.input_manager.key_pressed(pg.K_F3):
            GameSettings.toggle_hitbox_debug()
        
        # --- Components ---
        # Tree Bark
        self.tree_bark.update(dt)
        
        # Wood Cutter
        self.wood_cutter.update(dt)
        
        # -- Branch --
        # Branches
        if self.state == Game.Playing:
            if self.branches:
                space = GameInfo.branch_space
                if self.branches[-1].y_dropped >= space:
                    self.add_new_branch()
                    #Logger.info(f"Branches: {' '.join([str(branch.y_dropped) for branch in self.branches])}")
                if not self.branches[0].show:
                    self.del_first_branch()
            
        for branch in self.branches:
            branch.update(dt)
            
        # -- Gem --
        # Gems
        if self.state == Game.Playing:
            space = GameInfo.branch_space
            if self.gems:
                if self.gems[-1].y_dropped >= space:
                    self.add_new_gem()
                    #Logger.info(f"Gems: {' '.join([str(gem.y_dropped) for gem in self.gems])}")
                if not self.gems[0].show:
                    self.del_first_gem()
            else:
                if self.branches and self.branches[-1].y_dropped >= space/2:
                    self.add_new_gem()
            
        for gem in self.gems:
            gem.update(dt)
    
    def draw_components(self, screen: pg.Surface) -> None:
        # Tree Bark
        self.tree_bark.draw(screen)
        
        # -- Branch --
        # Branches
        for branch in self.branches:
            branch.draw(screen)
        
        # -- Gem --
        # Gems
        for gem in self.gems:
            gem.draw(screen)
        
        # Wood Cutter
        self.wood_cutter.draw(screen)