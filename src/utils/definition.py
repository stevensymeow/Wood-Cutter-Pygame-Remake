from pygame import Rect
from .settings import GameSettings
from dataclasses import dataclass
from enum import Enum
from typing import overload, TypedDict, Protocol, Callable

MouseBtn = int
Key = int

Direction = Enum('Direction', ['UP', 'DOWN', 'LEFT', 'RIGHT', 'NONE'])

@dataclass
class Position:
    x: float
    y: float
    
    def copy(self):
        return Position(self.x, self.y)
        
    def distance_to(self, other: "Position") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        
@dataclass
class PositionCamera:
    x: int
    y: int
    
    def copy(self):
        return PositionCamera(self.x, self.y)
        
    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
        
    def transform_position(self, position: Position) -> tuple[int, int]:
        return (int(position.x) - self.x, int(position.y) - self.y)
        
    def transform_position_as_position(self, position: Position) -> Position:
        return Position(int(position.x) - self.x, int(position.y) - self.y)
        
    def transform_rect(self, rect: Rect) -> Rect:
        return Rect(rect.x - self.x, rect.y - self.y, rect.width, rect.height)
    
    # relative position: because my math is sooo bad
    def relative_position(self, position: Position) -> tuple[int, int]:
        return (int(position.x) + self.x, int(position.y) + self.y)
    
    def relative_position_as_position(self, position: Position) -> Position:
        return Position(int(position.x) + self.x, int(position.y) + self.y)
    
    def relative_rect(self, rect: Rect) -> Rect:
        return Rect(rect.x + self.x, rect.y + self.y, rect.width, rect.height)

@dataclass
class Teleport:
    pos: Position
    destination: str
    
    # teleport to designated position
    dest_pos: Position
    
    # check teleport direction
    direction: Direction
    
    @overload
    def __init__(self, x: int, y: int, destination: str) -> None: ...
    @overload
    def __init__(self, pos: Position, destination: str) -> None: ...

    def __init__(self, *args, **kwargs):
        if isinstance(args[0], Position):
            self.pos = args[0]
            self.destination = args[1]
        else: # actually uses this
            """
            x, y, dest = args
            self.pos = Position(x, y)
            self.destination = dest
            """
            size = GameSettings.TILE_SIZE
            if len(args) == 3:
                x, y, dest = args
                self.pos = Position(x * size, y * size)
                self.destination = dest
            elif len(args) == 6:
                # teleport to designated position
                x, y, dest, dest_x, dest_y, direction_str = args
                self.pos = Position(x * size, y * size)
                self.destination = dest
                self.dest_pos = Position(dest_x * size, dest_y * size)
                # check teleport direction
                match direction_str:
                    case "RIGHT":
                        self.direction = Direction.RIGHT
                    case "LEFT":
                        self.direction = Direction.LEFT
                    case "DOWN":
                        self.direction = Direction.DOWN
                    case "UP":
                        self.direction = Direction.UP
                
                
            # teleport to designated position
            """
            self.dest_pos = Position(0, 0) # MUST BE COMMENTED OFF, set value and excuted GameManager.save() to make it more convenient to modify game0.json
            """
            # check teleport direction
            """
            self.direction = Direction.UP # MUST BE COMMENTED OFF, set value and excuted GameManager.save() to make it more convenient to modify game0.json
            """
    
    def to_dict(self):
        if not (self.dest_pos and self.direction):
            return {
                "x": self.pos.x // GameSettings.TILE_SIZE,
                "y": self.pos.y // GameSettings.TILE_SIZE,
                "destination": self.destination
            }
        else:
            # teleport to designated position
            # check teleport direction
            match self.direction:
                case Direction.RIGHT:
                    direction_str = "RIGHT"
                case Direction.LEFT:
                    direction_str = "LEFT"
                case Direction.DOWN:
                    direction_str = "DOWN"
                case Direction.UP:
                    direction_str = "UP"
            
            return {
                "x": self.pos.x // GameSettings.TILE_SIZE,
                "y": self.pos.y // GameSettings.TILE_SIZE,
                "destination": self.destination,
                "dest_x": self.dest_pos.x // GameSettings.TILE_SIZE,
                "dest_y": self.dest_pos.y // GameSettings.TILE_SIZE,
                "direction": direction_str
            }
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        return cls(data["x"] * GameSettings.TILE_SIZE, data["y"] * GameSettings.TILE_SIZE, data["destination"])
        """
        # teleport to designated position
        # check teleport direction
        return cls(*[val for key, val in data.items()])

# For navigate
@dataclass
class Place:
    name: str
    pos: Position
    
    def __init__(self, name: str, x: int, y: int):
        self.name = name
        
        size = GameSettings.TILE_SIZE
        self.pos = Position(x * size, y * size)
    
    def get_coor(self) -> tuple[float, float]:
        size = GameSettings.TILE_SIZE
        return (self.pos.x / size, self.pos.y / size)
    
    def to_dict(self):
        size = GameSettings.TILE_SIZE
        return {
            "name": self.name,
            "x": self.pos.x / size,
            "y": self.pos.y / size
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

# For battle
class Skill(TypedDict):
    anim: int # for skill_index
    name: str
    power: int
    accuracy: int

class Element(Enum):
    Grass = "Grass"
    Water = "Water"
    Fire = "Fire"
    Normal = "Normal"
    Mystery = "Mystery"

class Effect(TypedDict):
    hp: int
    attack: int
    defense: int
    duration: int
  
class Monster(TypedDict):
    index: int
    name: str
    hp: int
    max_hp: int
    level: int
    sprite_path: str
    # For battle
    element: Element
    attack: int 
    defense: int
    skills: list[Skill]
    # For evolution
    evolve_level: int
    evolve_index: int
    # Effects
    effects: list[Effect]
    # Captured
    captured: bool # use as int

class Item(TypedDict):
    index: int
    name: str
    count: int
    sprite_path: str
    # For game
    game: bool
    # For battle
    battle: bool
    # Effect
    effect: Effect
    
class Trade(TypedDict):
    cost: Item
    gain: Item

# For online
class OnlinePlayer(TypedDict):
    id: int
    x: float
    y: float
    map: str
    dir: str
    moving: bool
    name: str
    skin: str

# For interact frame
class FrameConfig(TypedDict):
    display_str: str
    display_str_2: str
    skill_str_1: str
    skill_str_2: str
    skill_str_3: str
    button1_str: str
    button1_on_click: Callable[[], None] | None = None
    button2_str: str
    button2_on_click: Callable[[], None] | None = None
    button3_str: str
    button3_on_click: Callable[[], None] | None = None
    button4_str: str
    button4_on_click: Callable[[], None] | None = None