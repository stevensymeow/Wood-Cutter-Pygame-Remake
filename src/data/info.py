import pygame as pg
import json, os

from src.utils import GameSettings, Logger, load_data, ASSETS_DIR, SAVES_DIR
from src.levels import Level, LevelInfo
from src.interface.dialogs import tk_level_select

class Info:
    # json path
    path: int
    
    # version
    version: str = "v0"
    
    # Info
    bark_width: int = 80
    branch_width: int = 150
    branch_height: int = 40
    gem_width: int = 40
    gem_height: int = 80
    branch_space: int = 300
    wood_cutter_width: int = 80
    
    # Levels
    levels: list[Level]
    level_datas: list[LevelInfo]
    level_count: int

    def __init__(self):
        self.path = str(ASSETS_DIR / "data" / "info0.json")
        
        # Levels
        self.levels = []
        self.level_count = 0
        #self.levels.append(Level())
    
    def show(self):
        Logger.info(f"GameInfo: {self.__dict__}")
    
    # -- Levels --
    def to_next_level(self) -> bool:
        if GameSettings.level_index < self.level_count - 1:
            GameSettings.level_index += 1
            Logger.info(f"Moved to next level: {GameSettings.level_index}")
            GameSettings.LEVEL_SWITCHED = True
            return True
        return False
    
    def to_prev_level(self) -> bool:
        if GameSettings.level_index > 0:
            GameSettings.level_index -= 1
            Logger.info(f"Moved to previous level: {GameSettings.level_index}")
            GameSettings.LEVEL_SWITCHED = True
            return True
        return False

    def select_levels(self) -> bool:
        """Select level API"""
        icon_path = ASSETS_DIR / "images/window_icon/mochicat.ico"
        level_index = tk_level_select(self.level_datas, GameSettings.level_index, icon_path=icon_path)
        if level_index != GameSettings.level_index:
            return self.set_level(level_index)
        return False
    
    def set_level(self, level_index: int) -> bool:
        if 0 <= level_index <= self.level_count - 1 and GameSettings != level_index:
            GameSettings.level_index = level_index
            Logger.info(f"Moved to level: {level_index}")
            return True
        return False
    # -- Levels --
    
    def save(self) -> None:
        try:
            path = self.path
            with open(path, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
            Logger.info(f"Info saved to {path}")
        except Exception as e:
            Logger.warning(f"Failed to save info: {e}")
    
    def to_dict(self) -> dict[str, object]:
        # Levels
        level_datas: list[dict[str, object]] = []
        for level in self.levels:
            level_datas.append(level.to_dict())
        
        return {
            "version": self.version,
            "bark_width": self.bark_width,
            "branch_width": self.branch_width,
            "branch_height": self.branch_height,
            "gem_width": self.gem_width,
            "gem_height": self.gem_height,
            "branch_space": self.branch_space,
            "wood_cutter_width": self.wood_cutter_width,
            "levels": level_datas
        }

    # Load info
    def load_info(self):
        path = str(ASSETS_DIR / "data" / "info0.json")
        if not os.path.exists(path):
            Logger.error(f"No file found: {path}, ignoring info load function")
            return None

        with open(path, "r") as f:
            data: dict[str, object] = json.load(f)
        
        self.version = data.get("version") or self.version
        
        self.bark_width = data.get("bark_width") or self.bark_width
        self.branch_width = data.get("branch_width") or self.branch_width
        self.branch_height = data.get("branch_height") or self.branch_height
        self.gem_width = data.get("gem_width") or self.gem_width
        self.gem_height = data.get("gem_height") or self.gem_height
        self.branch_space = data.get("branch_space") or self.branch_space
        self.wood_cutter_width = data.get("wood_cutter_width") or self.wood_cutter_width
        
        # Levels
        level_datas: list[LevelInfo] = data.get("levels") or []
        self.level_datas = level_datas
        for level_data in level_datas:
            self.levels.append(Level.from_dict(level_data))
        self.level_count = len(self.levels)
    

GameInfo = Info()
GameInfo.load_info()
if (GameSettings.DEBUG): GameInfo.save()
#GameInfo.show()
