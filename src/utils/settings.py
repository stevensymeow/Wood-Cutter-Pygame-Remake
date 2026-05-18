import pygame as pg
import json, os
from pathlib import Path
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from src.utils import Logger
    from src.utils.loader import ASSETS_DIR, SAVES_DIR, CONFIG_DIR

@dataclass
class Settings:
    # Screen
    DEFAULT_WIDTH: int = 1000   # The default width of the game window: 1280
    DEFAULT_HEIGHT: int = 720   # The default height of the game window: 720
    SAVE_WIDTH: int = 1000      # The window height to save
    SAVE_HEIGHT: int = 720      # The window width to save
    SCREEN_MAXIMIZED: bool = False
    SCREEN_WIDTH: int = 1000    # Width of the game window: 1000 | 1920(fills)
    SCREEN_HEIGHT: int = 720    # Height of the game window: 720 | 1080(fills) 1009
    FPS: int = 60               # Frames per second
    TITLE: str = "Wood Cutter v0"    # Title of the game window
    DEBUG: bool = True         # Debug mode; True
    TILE_SIZE: int = 64         # Size of each tile in pixels
    DRAW_HITBOXES: bool = False # Draw hitboxes for debugging; True
    # Version
    VERSION: str = "v0"
    # Audio
    MAX_CHANNELS: int = 16
    AUDIO_VOLUME: float = 0.5   # Volume of audio
    AUDIO_MUTE: bool = False
    # Online
    IS_ONLINE: bool = False
    ONLINE_SERVER_IP: str = "127.0.0.1"
    ONLINE_SERVER_URL: str = "http://127.0.0.1:8989"
    # Text
    TEXT_FONT: str = "Minecraft.ttf"
    INSTRUCTION_TEXT_FONT: str = "CambriaBold.ttf"
    # Auto save
    AUTO_SAVE: bool = True
    # Json Paths
    CONFIG_JSON: str = "config.json"
    
    def set_volume(self, volume: float):
        self.AUDIO_VOLUME = volume
        
    def toggle_mute(self):
        if self.AUDIO_MUTE:
            self.AUDIO_MUTE = False
        else:
            self.AUDIO_MUTE = True
    
    def toggle_hitbox_debug(self):
        if self.DRAW_HITBOXES:
            self.DRAW_HITBOXES = False
        else:
            self.DRAW_HITBOXES = True
    
    # Set screen size
    def set_screen_size(self, screen_width: int, screen_height: int):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
    
    def default_screen_size(self):
        if self.SCREEN_MAXIMIZED:
            return
        self.SCREEN_WIDTH = self.DEFAULT_WIDTH
        self.SCREEN_HEIGHT = self.DEFAULT_HEIGHT
    
    # Check screen size save
    def check_screen_save(self):
        from src.utils import Logger
        if (self.SAVE_WIDTH != self.SCREEN_WIDTH) or (self.SAVE_HEIGHT != self.SCREEN_HEIGHT):
            print(self.SCREEN_MAXIMIZED)
            if not self.SCREEN_MAXIMIZED:
                Logger.info("Not maximized, will save size")
                self.SAVE_WIDTH  = self.SCREEN_WIDTH
                self.SAVE_HEIGHT = self.SCREEN_HEIGHT
            else:
                Logger.info("Maximized, will not save size")
    
    # Set title
    def set_title(self, title: str):
        self.TITLE = title
        
        # Online rename
        if self.IS_ONLINE:
            self.TITLE = self.TITLE.replace("Offline", "Online")
        else:
            self.TITLE = self.TITLE.replace("Online", "Offline")
            
        # Version rename
        for t in title.split():
            if t.lower().startswith("v"):
                print(t)
                self.TITLE = self.TITLE.replace(t, self.VERSION)
                break
    
    # Save Config
    def to_config_dict(self) -> dict[str, object]:
        self.check_screen_save()
        return {
            "SCREEN_WIDTH": self.SAVE_WIDTH,
            "SCREEN_HEIGHT": self.SAVE_HEIGHT,
            "TITLE": self.TITLE,
            "DEBUG": "True" if self.DEBUG else "False",
            "AUTO_SAVE": "True" if self.AUTO_SAVE else "False"
        }
    
    def save_config(self, do_log: bool = True):
        if do_log: from src.utils import Logger
        try:
            path = self.CONFIG_JSON
            with open(path, "w") as f:
                json.dump(self.to_config_dict(), f, indent=2)
            if do_log: Logger.info(f"Config saved to {path}")
        except Exception as e:
            if do_log: Logger.warning(f"Failed to save config: {e}")
    
    # Load config except path, when init
    def load_config_except_path(self):
        path = self.CONFIG_JSON
        if not os.path.exists(path):
            # In case accidental deletion of config
            data: dict[str, object] = {}
            # Make config file
            self.save_config(do_log=False)
        else:
            with open(path, "r") as f:
                data: dict[str, object] = json.load(f)
        
        screen_width = data.get("SCREEN_WIDTH") or self.SCREEN_WIDTH
        screen_height = data.get("SCREEN_HEIGHT") or self.SCREEN_HEIGHT
        title = data.get("TITLE") or self.TITLE
        debug = data.get("DEBUG") or "False"
        auto_save = data.get("AUTO_SAVE") or "True"
        
        self.set_screen_size(screen_width, screen_height)
        self.set_title(title)
        self.DEBUG = (debug == "True")
        self.AUTO_SAVE = (auto_save != "False")
    
GameSettings = Settings()
GameSettings.load_config_except_path()
