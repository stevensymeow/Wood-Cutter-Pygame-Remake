from __future__ import annotations
from src.utils import Logger, GameSettings
import pygame as pg
from enum import Enum
import random
import json
import os
from typing import Callable
from typing import TYPE_CHECKING
from src.data.info import GameInfo
from src.levels import Level
from src.utils.definition import RGBColor, Record
from src.utils import SAVES_DIR

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
    
    # Levels
    levels: list[Level]
    level_count: int
    level_index: int
    
    # -- Features --
    # Branch move
    branch_count_m: int
    move_count: int     # count until next move
    branch_move: bool   # whether branches will move
    
    # Branch emerge
    branch_count_e: int
    emerge_count: int     # count until next emergin
    branch_emerge: bool   # whether branches will emerge
    
    # --- Components ---
    # Tree Bark
    tree_bark: Rectangle
    
    # Wood Cutter
    wood_cutter: WoodCutter
    
    # -- Branches --
    branches: list[Branch]
    make_new_branch: Callable[[int, bool, bool], Branch]
    
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
        
        # Levels
        self.levels = GameInfo.levels[:]
        self.level_count = len(self.levels)
        self.level_index = GameSettings.level_index
        
        # --- Features ---
        # Branch move
        self.branch_count_m = 0
        self.move_count = random.randint(1, 4)
        self.branch_move = False
        
        # Branch emerge
        self.branch_count_e = 0
        self.emerge_count = random.randint(1, 4)
        self.branch_emerge = False
        
        # --- Components ---
        # Branches
        self.branches = []
        # Gems
        self.gems = []
        
        # Level Records
        self.load_record()
    
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
        
        def new_branch(pos: int = -1, 
                       do_move: bool = False,
                       do_emerge: bool = False) -> Branch:
            return Branch(gm, pos=pos, do_move=do_move, do_emerge=do_emerge)
        gm.make_new_branch = new_branch
        
        # -- Gems --
        gm.gems = []
        
        def new_gem(pos: int = -1) -> Gem:
            return Gem(gm, pos=pos)
        gm.make_new_gem = new_gem
        
        return gm

    # -- Levels --
    @property
    def curr_lv(self) -> Level:
        self.level_index = GameSettings.level_index
        return self.levels[self.level_index]
    
    @property
    def has_next_level(self) -> bool:
        self.level_index = GameSettings.level_index
        return self.level_index < self.level_count - 1
    
    @property
    def has_prev_level(self) -> bool:
        self.level_index = GameSettings.level_index
        return self.level_index > 0
    # -- Levels --
    
    # -- Branches --
    def add_new_branch(self, count: int = 1):
        for _ in range(count):
            pos = random.randint(0, 1)*2 - 1
            
            # --- Features ---
            # Lv2: Branch Move
            self.branch_count_m += 1
            branch_move = False
            if self.branch_count_m > self.move_count:
                branch_move = True
                self.branch_count_m = 0
                self.move_count = random.randint(1, 4)
            # Lv3: Branch Emerge
            self.branch_count_e += 1
            branch_emerge = False
            if self.branch_count_e > self.emerge_count:
                branch_emerge = True
                self.branch_count_e = 0
                self.emerge_count = random.randint(1, 4)
            
            self.branches.append(self.make_new_branch(pos, branch_move, branch_emerge))
    
    def del_first_branch(self):
        self.branches.pop(0)
    
    def del_all_branches(self):
        self.branches.clear()
    # -- Branches --
    
    # -- Gems --
    def add_new_gem(self, count: int = 1):
        for _ in range(count):
            pos = random.randint(0, 1)*2 - 1
            self.gems.append(self.make_new_gem(pos))
    
    def del_first_gem(self):
        self.gems.pop(0)
    
    def del_all_gems(self):
        self.gems.clear()
    # -- Gems --
    
    def enter(self) -> None:
        self.state = Game.Entered
        self.game_init()
        # Record
        self.highest_score = self.curr_lv.highest_score
        # Player color
        self.wood_cutter.set_color(self.curr_lv.player_color)
    
    def exit(self) -> None:
        self.state = Game.Entered
        self.game_init()
    
    def end_game(self):
        self.state = Game.GG
        self.sound_manager.play_sound(self.curr_lv.gg_bgm)
        self.set_record()
    
    def set_record(self):
        record: Record = {"score": self.score, "branches": self.fallen_branches, "gems": self.collected_gems}
        self.curr_lv.set_record(record)
        if GameSettings.AUTO_SAVE: self.save()
    
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
        # Level index
        self.level_index = GameSettings.level_index
        
        # State
        match (self.state):
            case Game.Entered:
                left_bound = self.wood_cutter.x_left - self.wood_cutter.width/2
                right_bound = self.wood_cutter.x_right + self.wood_cutter.width/2
                start_condition = self.input_manager.key_pressed(pg.K_LEFT) or self.input_manager.key_pressed(pg.K_RIGHT) or \
                                  self.input_manager.key_pressed(pg.K_a) or self.input_manager.key_pressed(pg.K_d) or \
                    (self.input_manager.mouse_pressed(1) and left_bound <= self.input_manager.mouse_pos[0] <= right_bound)
                if start_condition:
                    self.game_init()
                    self.state = Game.Playing
                    self.sound_manager.play_bgm(self.curr_lv.bgm_path)
                    #self.sound_manager.play_bgm("dance celebrate.wav")
                    self.add_new_branch()
                    #self.add_new_gem()
            case Game.Playing:
                # Pause
                if self.input_manager.key_pressed(pg.K_SPACE):
                    self.state = Game.Paused
                    self.sound_manager.pause_all()
                    Logger.info("Game paused!")
                # Score
                self.score = self.collected_gems + self.fallen_branches
                if self.score > self.highest_score:
                    self.highest_score = self.score
            case Game.Paused:
                # Resume
                if self.input_manager.key_pressed(pg.K_SPACE):
                    self.state = Game.Playing
                    self.sound_manager.resume_all()
                    Logger.info("Game resumed!")
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
                if not self.branches[0].falling:
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
                if not self.gems[0].falling:
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
        
    def to_dict(self) -> dict[str, object]:
        data: dict[str, object] = {}
        data["level_index"] = self.level_index
        data["level_label"] = self.curr_lv.level_label
        data["level_name"] = self.curr_lv.level_name
        data["levels"] = [level.records_to_dict() for level in self.levels]
        return data
    
    def save(self):
        try:
            path = str(SAVES_DIR / "records0.json")
            with open(path, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
            Logger.info(f"Record saved to {path}")
        except Exception as e:
            Logger.warning(f"Failed to save record: {e}")
    
    def load_record(self):
        path = str(SAVES_DIR / "records0.json")
        if not os.path.exists(path):
            Logger.info(f"No record file found: {path}, making it")
            self.save()
            return None

        with open(path, "r") as f:
            data: dict[str, object] = json.load(f)
        
        level_data: list[dict[str, object]] = data["levels"]
        for i in range(self.level_count):
            self.levels[i].load_record(level_data[i])
        