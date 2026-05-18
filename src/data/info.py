import pygame as pg
import json, os
from src.utils import GameSettings, Logger, load_data, ASSETS_DIR, SAVES_DIR

class Info:
    # json path
    path: int
    
    # Info
    bark_width: int = 80
    branch_width: int = 150
    branch_height: int = 40
    gem_width: int = 40
    gem_height: int = 80
    branch_space: int = 300
    wood_cutter_width: int = 80
    gravity: int = 5

    def __init__(self):
        self.path = str(ASSETS_DIR / "info0.json")
    
    def show(self):
        Logger.info(f"GameInfo: {self.__dict__}")
    
    def save(self) -> None:
        try:
            path = self.path
            with open(path, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
            Logger.info(f"Info saved to {path}")
        except Exception as e:
            Logger.warning(f"Failed to save info: {e}")
    
    def to_dict(self) -> dict[str, object]:
        return {
            "bark_width": self.bark_width,
            "branch_width": self.branch_width,
            "branch_height": self.branch_height,
            "gem_width": self.gem_width,
            "gem_height": self.gem_height,
            "branch_space": self.branch_space,
            "wood_cutter_width": self.wood_cutter_width,
            "gravity": self.gravity,
        }

    # Load info
    def load_info(self):
        path = str(ASSETS_DIR / "info0.json")
        if not os.path.exists(path):
            Logger.error(f"No file found: {path}, ignoring load function")
            return None

        with open(path, "r") as f:
            data: dict[str, object] = json.load(f)
        
        self.bark_width = data.get("bark_width") or self.bark_width
        self.branch_width = data.get("branch_width") or self.branch_width
        self.branch_height = data.get("branch_height") or self.branch_height
        self.gem_width = data.get("gem_width") or self.gem_width
        self.gem_height = data.get("gem_height") or self.gem_height
        self.branch_space = data.get("branch_space") or self.branch_space
        self.wood_cutter_width = data.get("wood_cutter_width") or self.wood_cutter_width
        self.gravity = data.get("gravity") or self.gravity
    

GameInfo = Info()
GameInfo.load_info()
if (GameSettings.DEBUG): GameInfo.save()
#GameInfo.show()
