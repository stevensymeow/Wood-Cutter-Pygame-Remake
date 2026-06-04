import pygame as pg
import json
from src.utils import GameSettings, Logger
from src.utils.definition import RGBColor, Record
from typing import TypedDict

class LevelInfo(TypedDict):
    # Names
    level_label: str
    level_name: str
    # Sound
    bgm_path: str
    gg_bgm: str
    # Color
    background_color: RGBColor
    title_color: RGBColor
    button_color: RGBColor
    player_color: RGBColor
    score_color: RGBColor
    text_color: RGBColor
    # Speed
    fall_speed: int
    branch_move_speed: int
    branch_emerge_speed: int
    gravity: int
    # Features
    branch_move: bool
    move_sound: str
    branch_emerge: bool
    emerge_sound: str
    highest_score: int
    # Records
    records: list[Record]

class Level:
    # Names
    level_label: str = "Lv1"
    level_name: str = "Normal Tree"
    
    # Sound
    bgm_path: str = "xylo1.wav"
    gg_bgm: str = "cave.wav"
    
    # Colors
    background_color: RGBColor = (0, 255, 255)
    title_color: RGBColor = (255, 0, 0)
    button_color: RGBColor = (255, 125, 0)
    player_color: RGBColor = (0, 0, 0)
    score_color: RGBColor = (0, 0, 0)
    text_color: RGBColor = (255, 0, 0)
    
    # Speed
    fall_speed: int = 7
    branch_move_speed: int = 10
    branch_emerge_speed: int = 15
    gravity: int = 1
    
    # Features
    branch_move: bool = False       # Level 2
    move_sound: str = "Teleport2.wav"
    branch_emerge: bool = False     # Level 3
    emerge_sound: str = "Emerge.wav"
    
    # Records (class defaults kept for typing, but instances will override)
    highest_score: int = 0
    records: list[Record] = []

    def __init__(self):
        # Instance-specific records and highest score to avoid shared mutable defaults
        self.highest_score = 0
        self.records: list[Record] = []
    
    def __repr__(self) -> str:
        return json.dumps(self.to_dict())
    
    def validate_gravity(self):
        if self.gravity > 0:
            self.gravity = 1
        elif self.gravity < 0:
            self.gravity = -1
        else:
            self.gravity = 1
    
    def toggle_gravity(self):
        self.gravity = -self.gravity
        self.validate_gravity()
    
    def make_block(self) -> LevelInfo:
        block: LevelInfo = {
            "level_label": self.level_label,
            "level_name": self.level_name,
            "bgm_path": self.bgm_path,
            "gg_bgm": self.gg_bgm,
        }
        return block
    
    def to_dict(self) -> LevelInfo:
        block: LevelInfo = self.make_block()
        
        # Color
        block["background_color"] = self.background_color
        block["title_color"] = self.title_color
        block["button_color"] = self.button_color
        block["player_color"] = self.player_color
        block["score_color"] = self.score_color
        block["text_color"] = self.text_color
        
        # Speed
        block["fall_speed"] = self.fall_speed
        block["branch_move_speed"] = self.branch_move_speed
        block["branch_emerge_speed"] = self.branch_emerge_speed
        block["gravity"] = self.gravity

        # Features
        block["branch_move"] = self.branch_move
        block["move_sound"] = self.move_sound
        block["branch_emerge"] = self.branch_emerge
        block["emerge_sound"] = self.emerge_sound
        
        return block
    
    def records_to_dict(self) -> LevelInfo:
        block: LevelInfo = self.make_block()
        
        # Records
        block["highest_score"] = self.highest_score
        block["records"] = self.records
        
        return block
    
    def set_record(self, record: Record):
        if record["score"] == 0: return
        if (record["branches"] + record["gems"]) != record["score"]: return
        recorded = False
        if (self.records):
            highest_record = self.records[0]
            if record["score"] >= highest_record["score"] and record != highest_record:
                self.records.insert(0, record)
                recorded = True
        else:
            self.records.append(record)
            recorded = True
        self.highest_score = self.records[0]["score"]
        if recorded:
            Logger.info(f"{self.level_label} set record {self.highest_score}!")
    
    def load_record(self, data: LevelInfo):
        self.highest_score = data.get("highest_score") or 0
        self.records = data.get("records") or []
    
    @classmethod
    def from_dict(cls, data: LevelInfo) -> "Level":
        level = cls()
        
        # Labels
        level.level_label = data.get("level_label") or level.level_label
        level.level_name = data.get("level_name") or level.level_name
        
        # Sounds
        level.bgm_path = data.get("bgm_path") or level.bgm_path
        level.gg_bgm = data.get("gg_bgm") or level.gg_bgm
        
        # Colors
        level.background_color = data.get("background_color") or level.background_color
        level.title_color = data.get("title_color") or level.title_color
        level.button_color = data.get("button_color") or level.button_color
        level.player_color = data.get("player_color") or level.player_color
        level.score_color = data.get("score_color") or level.score_color
        level.text_color = data.get("text_color") or level.text_color
        
        # Speed
        level.fall_speed = data.get("fall_speed") or level.fall_speed
        level.branch_move_speed = data.get("branch_move_speed") or level.branch_move_speed
        level.branch_emerge_speed = data.get("branch_emerge_speed") or level.branch_emerge_speed
        level.gravity = data.get("gravity") or level.gravity
        level.validate_gravity()
        
        # Features
        level.branch_move = data.get("branch_move") or level.branch_move
        level.move_sound = data.get("move_sound") or level.move_sound
        level.branch_emerge = data.get("branch_emerge") or level.branch_emerge
        level.emerge_sound = data.get("emerge_sound") or level.emerge_sound
        
        return level
